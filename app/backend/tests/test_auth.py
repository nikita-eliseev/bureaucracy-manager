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
    
async def test_me(client, access_token):
    response = await client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200
    
@pytest.mark.asyncio
async def test_refresh_token(auth_client, refresh_token):
    response = await auth_client.post(
        "/auth/refresh",
        json={
            "refresh_token": refresh_token
        }
    )
    
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_login_wrong_password(client, prepared_db):
    await client.post("/auth/register", json={
        "email": "wrongpass@test.com",
        "password": "123456"
    })

    response = await client.post("/auth/login", json={
        "email": "wrongpass@test.com",
        "password": "WRONG"
    })

    assert response.status_code == 400
    
@pytest.mark.asyncio
async def test_login_user_not_found(client):
    response = await client.post("/auth/login", json={
        "email": "no@user.com",
        "password": "123456"
    })

    assert response.status_code == 400
    
@pytest.mark.asyncio
async def test_register_invalid_email(client):
    response = await client.post("/auth/register", json={
        "email": "not-an-email",
        "password": "123456"
    })

    assert response.status_code == 422
    
@pytest.mark.asyncio
async def test_register_empty_password(client):
    response = await client.post("/auth/register", json={
        "email": "test2@test.com",
        "password": ""
    })

    assert response.status_code == 422
    
@pytest.mark.asyncio
async def test_refresh_token_reuse_fails(auth_client, refresh_token):
    r1 = await auth_client.post("/auth/refresh", json={
        "refresh_token": refresh_token
    })

    assert r1.status_code == 200

    r2 = await auth_client.post("/auth/refresh", json={
        "refresh_token": refresh_token
    })

    assert r2.status_code in (401, 400)