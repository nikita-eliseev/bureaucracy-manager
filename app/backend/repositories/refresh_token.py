from sqlalchemy import delete, select

from app.backend.models.refresh_token import RefreshToken
from sqlalchemy.ext.asyncio import AsyncSession

class RefreshTokenRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        
    async def create(self, user_id: str, token: str, expire_at) -> RefreshToken:
        refresh_token = RefreshToken(
            user_id=user_id,
            token=token,
            expire_at=expire_at
        )
        
        self.db.add(refresh_token)
        
    async def get(self, token: str):
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.token == token)
        )
    
        return result.scalar_one_or_none()
    
    async def delete(self, token: str):
        await self.db.execute(
            delete(RefreshToken).where(RefreshToken.token == token)
        )