from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.core.database import AsyncSessionLocal
from app.backend.services.auth import AuthService


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        
async def get_auth_serivece(db: AsyncSession = Depends(get_db)):
    return AuthService(db=db)