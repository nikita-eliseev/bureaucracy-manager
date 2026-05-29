import os

from httpx import ASGITransport, AsyncClient

import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.backend.core.dependencies import get_db
from app.backend.core.database import Base
from main import app


TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

#   TEST_DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5433/postgres"

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