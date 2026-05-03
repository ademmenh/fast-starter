import pytest
from httpx import AsyncClient
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncEngine
from src.users.infrastructure.schema import users_table

# ── login ─────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_login_with_unknown_email_returns_401(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@example.com", "password": "password123"},
    )
    assert response.status_code == 401
    assert response.json()["error"] == "UNAUTHORIZED"


@pytest.mark.asyncio
async def test_login_with_wrong_password_returns_401(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"name": "Alice Auth", "email": "alice.auth@example.com", "password": "correct"},
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "alice.auth@example.com", "password": "wrong"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_returns_access_and_refresh_tokens(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"name": "Bob Auth", "email": "bob.auth@example.com", "password": "bobpass"},
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "bob.auth@example.com", "password": "bobpass"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "accessToken" in data["tokens"]
    assert "refreshToken" in data["tokens"]
    assert data["data"]["email"] == "bob.auth@example.com"
    assert data["message"] == "Login successful"
    assert data["statusCode"] == 200


# ── register ──────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_register_returns_tokens_and_201(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={"name": "Carol Auth", "email": "carol.auth@example.com", "password": "carolpass"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "accessToken" in data["tokens"]
    assert "refreshToken" in data["tokens"]
    assert data["data"]["email"] == "carol.auth@example.com"
    assert data["data"]["role"] == "client"
    assert data["statusCode"] == 201


@pytest.mark.asyncio
async def test_register_duplicate_email_returns_409(client: AsyncClient):
    payload = {"name": "Dave Auth", "email": "dave.auth@example.com", "password": "davepass"}
    await client.post("/api/v1/auth/register", json=payload)
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 409
    assert response.json()["error"] == "CONFLICT"


@pytest.mark.asyncio
async def test_register_access_token_is_usable(client: AsyncClient, db_engine: AsyncEngine):
    email = "eve.auth@example.com"
    password = "evepass"
    reg = await client.post(
        "/api/v1/auth/register",
        json={"name": "Eve Auth", "email": email, "password": password},
    )
    user_id = reg.json()["data"]["id"]
    
    # Elevate to admin in DB
    async with db_engine.begin() as conn:
        await conn.execute(
            update(users_table).where(users_table.c.id == user_id).values(role="admin")
        )
    
    # Login again to get a token with the 'admin' role in the payload
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    token = login_resp.json()["tokens"]["accessToken"]
    
    me = await client.get(
        f"/api/v1/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me.status_code == 200
    assert me.json()["data"]["email"] == email


# ── refresh ───────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_refresh_returns_new_tokens(client: AsyncClient):
    reg = await client.post(
        "/api/v1/auth/register",
        json={"name": "Frank Auth", "email": "frank.auth@example.com", "password": "frankpass"},
    )
    original_refresh = reg.json()["tokens"]["refreshToken"]

    response = await client.post(
        "/api/v1/auth/refresh",
        headers={"Authorization": f"Bearer {original_refresh}"},
    )
    assert response.status_code == 200
    data = response.json()
    # The current implementation returns ApiResponse[AuthTokensRDTO], so tokens are in data["data"]
    assert "accessToken" in data["data"]
    assert "refreshToken" in data["data"]


@pytest.mark.asyncio
async def test_refresh_new_access_token_is_usable(client: AsyncClient, db_engine: AsyncEngine):
    email = "grace.auth@example.com"
    password = "gracepass"
    reg = await client.post(
        "/api/v1/auth/register",
        json={"name": "Grace Auth", "email": email, "password": password},
    )
    user_id = reg.json()["data"]["id"]
    
    # Elevate to admin
    async with db_engine.begin() as conn:
        await conn.execute(
            update(users_table).where(users_table.c.id == user_id).values(role="admin")
        )

    # Login to get admin refresh token
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    refresh_token = login_resp.json()["tokens"]["refreshToken"]

    refresh_resp = await client.post(
        "/api/v1/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"},
    )
    assert refresh_resp.status_code == 200
    new_tokens = refresh_resp.json()["data"]

    me = await client.get(
        f"/api/v1/users/{user_id}",
        headers={"Authorization": f"Bearer {new_tokens['accessToken']}"},
    )
    assert me.status_code == 200


@pytest.mark.asyncio
async def test_refresh_with_invalid_token_returns_401(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/refresh",
        headers={"Authorization": "Bearer not.a.valid.token"},
    )
    assert response.status_code == 401
    assert response.json()["error"] == "UNAUTHORIZED"


@pytest.mark.asyncio
async def test_access_token_cannot_be_used_as_refresh_token(client: AsyncClient):
    reg = await client.post(
        "/api/v1/auth/register",
        json={"name": "Heidi Auth", "email": "heidi.auth@example.com", "password": "heidipass"},
    )
    access_token = reg.json()["tokens"]["accessToken"]

    response = await client.post(
        "/api/v1/auth/refresh",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 401
