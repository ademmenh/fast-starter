import pytest
from httpx import AsyncClient
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncEngine
from src.users.infrastructure.schema import users_table


@pytest.mark.asyncio
async def test_register_creates_client_user(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={"name": "Carol", "email": "carol@example.com", "password": "carol123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["email"] == "carol@example.com"
    assert data["data"]["role"] == "client"
    assert "passwordHash" not in data["data"]
    assert data["statusCode"] == 201


@pytest.mark.asyncio
async def test_register_duplicate_email_returns_409(client: AsyncClient):
    payload = {"name": "Dave", "email": "dave@example.com", "password": "dave123"}
    await client.post("/api/v1/auth/register", json=payload)
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 409
    assert response.json()["error"] == "CONFLICT"


@pytest.mark.asyncio
async def test_get_profile_requires_auth(client: AsyncClient):
    reg = await client.post(
        "/api/v1/auth/register",
        json={"name": "Eve", "email": "eve@example.com", "password": "eve1234"},
    )
    user_id = reg.json()["data"]["id"]
    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_authenticated_user_can_read_own_profile(client: AsyncClient, db_engine: AsyncEngine):
    email = "frank@example.com"
    password = "frank123"
    await client.post(
        "/api/v1/auth/register",
        json={"name": "Frank", "email": email, "password": password},
    )
    
    # Login as client (to get ID)
    login_init = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    user_id = login_init.json()["data"]["id"]
    
    # Elevate to admin
    async with db_engine.begin() as conn:
        await conn.execute(
            update(users_table).where(users_table.c.id == user_id).values(role="admin")
        )
    
    # Login again to get admin token
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    token = login.json()["tokens"]["accessToken"]

    response = await client.get(
        f"/api/v1/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["email"] == email
