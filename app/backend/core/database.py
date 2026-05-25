from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.backend.core.config import setting


session = create_async_engine(
    setting.database_url,
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

