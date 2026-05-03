import pytest
from httpx import AsyncClient


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
async def test_authenticated_user_can_read_own_profile(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"name": "Frank", "email": "frank@example.com", "password": "frank123"},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "frank@example.com", "password": "frank123"},
    )
    token = login.json()["tokens"]["accessToken"]
    user_id = login.json()["data"]["id"]

    response = await client.get(
        f"/api/v1/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["email"] == "frank@example.com"
