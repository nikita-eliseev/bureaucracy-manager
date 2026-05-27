from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.backend.core.config import settings


session = create_async_engine(
    settings.database_url,
    echo=True,
    future=True
)


AsyncSessionLocal = sessionmaker(
    bind=session,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass

