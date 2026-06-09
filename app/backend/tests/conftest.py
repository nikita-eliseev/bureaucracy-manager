from httpx import ASGITransport, AsyncClient

import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.backend.core.dependencies import get_db
from app.backend.core.database import Base
from main import app


TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)


TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(scope="session")
async def prepared_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture(autouse=True)
async def clean_db():
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(autouse=True)
def override_db():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac
        
@pytest_asyncio.fixture
async def test_user(client):
    response = await client.post(
        "/auth/reigster",
        json={
            "email": "test@test.com",
            "password": "123456"
        }
    )
    
    return response.json()

@pytest_asyncio.fixture
async def access_token(client):
    await client.post(
        "/auth/register",
        json={
            "email": "test@test.com",
            "password": "123456"
        }
    )
    
    response = await client.post(
        "/auth/login",
        json={
            "email": "test@test.com",
            "password": "123456"
        }
    )

    return response.json()["access_token"]

@pytest_asyncio.fixture
async def refresh_token(client):
    await client.post(
        "/auth/register",
        json={
            "email": "test@test.com",
            "password": "123456"
        }
    )
    
    response = await client.post(
        "/auth/login",
        json={
            "email": "test@test.com",
            "password": "123456"
        }
    )

    return response.json()["refresh_token"]

@pytest_asyncio.fixture
async def auth_client(client, access_token):
    client.headers.update(
        {
            "Authorization": f"Bearer {access_token}"
        }
    )

    return client