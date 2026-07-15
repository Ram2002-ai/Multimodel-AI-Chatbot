import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "new@example.com", "password": "Str0ngP@ss", "full_name": "New User"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_register_duplicate(client: AsyncClient):
    # Register first
    await client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "Str0ngP@ss"},
    )
    # Try again
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "AnotherP@ss"},
    )
    assert response.status_code == 409

@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    # Ensure user exists
    await client.post(
        "/api/v1/auth/register",
        json={"email": "login@example.com", "password": "Secret1!"},
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "Secret1!"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None

@pytest.mark.asyncio
async def test_login_invalid(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@example.com", "password": "wrong"},
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_me(client: AsyncClient):
    # Register and login
    await client.post(
        "/api/v1/auth/register",
        json={"email": "me@example.com", "password": "Test123!"},
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "me@example.com", "password": "Test123!"},
    )
    token = login_resp.json()["access_token"]
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"