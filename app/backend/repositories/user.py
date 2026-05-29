from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str):
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create_user(self, email: str, hashed_password: str) -> User:
        user = User(
            email=email, 
            hashed_password=hashed_password
        )
        
        self.db.add(user)
        return user