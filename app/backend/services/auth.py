from datetime import UTC, datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import JWTError
from app.backend.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.security import (
    create_access_token, 
    create_refresh_token,
    decode_token, 
    hash_password, 
    verify_password,
    hash_token
)
from app.backend.repositories.refresh_token import RefreshTokenRepository
from app.backend.repositories.user import UserRepository



class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UserRepository(db=db)
        self.refresh_token_repository = RefreshTokenRepository(db=db)
        
    async def register(self, email: str, password: str):
        existing = await self.user_repository.get_by_email(email=email)
        if existing:
            raise HTTPException( detail="User already exists", status_code=status.HTTP_400_BAD_REQUEST) 
        
        hashed = hash_password(password=password)
        
        user = await self.user_repository.create_user(email=email, hashed_password=hashed)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def login(self, email: str, password: str):
        user = await self.user_repository.get_by_email(email=email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid credentials"
            )  
        
        if not verify_password(password=password, hashed_password=user.hashed_password):
            raise HTTPException( detail="User does not exists", status_code=status.HTTP_400_BAD_REQUEST) 
        
        access = create_access_token(user.id)
        refresh = create_refresh_token(user.id)
        
        hashed_refresh = hash_token(refresh)
        
        
        expire_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
        
        await self.refresh_token_repository.create(
            user_id=user.id,
            token=hashed_refresh,
            expire_at=expire_at
        )
        print("USER:", user.email)
        print("RAW PASSWORD:", password)
        print("HASH:", user.hashed_password)

        print("VERIFY RESULT:", verify_password(password, user.hashed_password))
        await self.db.commit()
        return access, refresh
    
    async def refresh(self, refresh_token: str):
        db_token = await self.refresh_token_repository.get(hash_token(refresh_token))

        if not db_token:
            return None

        if db_token.revoked:
            return None
        
        expire_at = db_token.expire_at.replace(tzinfo=UTC)

        if expire_at < datetime.now(UTC):
            return None
        
        try:
            payload = decode_token(token=refresh_token)
            user_id = payload.get("sub")
            
            await self.db.commit()
            return create_access_token(user_id)

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refresh token error"
            )  
        
    async def logout(self, refresh_token: str):
        await self.refresh_token_repository.delete(hash_token(refresh_token))
        await self.db.commit()