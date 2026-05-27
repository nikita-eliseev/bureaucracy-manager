from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import JWTError
from app.backend.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.security import (
    create_access_token, 
    create_refresh_token,
    decode_token, 
    hash_password, 
    verify_password
)
from app.backend.repositories.refresh_token import RefreshTokenRepository
from app.backend.repositories.user import UserRepository



class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db=db)
        self.refresh_token_repository = RefreshTokenRepository(db=db)
        
    async def register(self, email: str, password: str):
        existing = await self.user_repository.get_by_email(email=email)
        if existing:
            raise HTTPException( detail="User already exists", status_code=status.HTTP_400_BAD_REQUEST)   #   change 
        
        hashed = hash_password(password=password)
        
        return await self.user_repository.create_user(email=email, hashed_password=hashed)
    
    async def login(self, email: str, password: str):
        user = await self.user_repository.get_by_email(email=email)
        
        if not user:
            raise Exception("User does not exists")   #   change 
        
        if not verify_password(password=password, hashed_password=user.hashed_password):
            raise Exception("Verify password is incorrect")
        
        access = create_access_token(user.id)
        refresh = create_refresh_token(user.id)
        expire_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
        
        await self.refresh_token_repository.create(
            user_id=user.id,
            token=refresh,
            expire_at=expire_at
        )
        return access, refresh
    
    async def refresh(self, refresh_token: str):
        db_token = await self.refresh_token_repository.get(refresh_token)

        if not db_token:
            return None
        
        try:
            payload = decode_token(token=refresh_token)
            user_id = payload.get("sub")

            return create_access_token(user_id)

        except JWTError:
            raise Exception("Refresh token error")   #   change 
        
    async def logout(self, refresh_token: str):
        await self.refresh_token_repository.delete(refresh_token)