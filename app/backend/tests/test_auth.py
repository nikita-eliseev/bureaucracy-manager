import pytest

@pytest.mark.asyncio
async def test_register(client, prepared_db):
    response = await client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "strongpassword"
        }
    )
    
    assert response.status_code == 201
    
    data = response.json()
    
    assert "id" in data
    
    assert data["email"] == "test@example.com"
    
@pytest.mark.asyncio
async def test_register_duplicate_email(client, prepared_db):
    await client.post(
        "/auth/register",
        json={
            "email": "dup@example.com",
            "password": "123456"
        }
    )
    
    response = await client.post(
        "/auth/register",
        json={
            "email": "dup@example.com",
            "password": "123456"
        }
    )
    
    assert response.status_code == 400
    
@pytest.mark.asyncio
async def test_login_success(client, prepared_db):
    await client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "123456"
        }
    )
    
    response = await client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "123456"            
        }
    )
    
    assert response.status_code == 200
    
    data = response.json()
    
    assert "access_token" in data
    assert "refresh_token" in data