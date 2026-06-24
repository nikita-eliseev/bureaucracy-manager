from datetime import UTC, datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import JWTError
from app.backend.core.logger import logger
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
            logger.warning(
                f"User already exists. user_id={existing.id}"
            )
            
            raise HTTPException( detail="User already exists", status_code=status.HTTP_400_BAD_REQUEST) 
        
        hashed = hash_password(password=password)
        
        user = await self.user_repository.create_user(email=email, hashed_password=hashed)
        await self.db.commit()
        await self.db.refresh(user)
        
        logger.info(
            f"User registered. user_id={user.id}"
        )
        
        return user
    
    async def login(self, email: str, password: str):
        user = await self.user_repository.get_by_email(email=email)
        
        if not user:
            logger.warning(
                "Invalid credentials."
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid credentials"
            )  
        
        if not verify_password(password=password, hashed_password=user.hashed_password):
            logger.warning(f"Invalid login attempt. email={email}")
            
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
        await self.db.commit()
        
        logger.info(f"User login. user_id={user.id}")
        
        return access, refresh
    
    async def refresh(self, refresh_token: str):
        try:
            payload = decode_token(refresh_token)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        user_id = payload.get("sub")

        db_token = await self.refresh_token_repository.get(
            hash_token(refresh_token)
        )

        if not db_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token not found"
            )

        if db_token.revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token revoked"
            )

        new_access = create_access_token(user_id)
        new_refresh = create_refresh_token(user_id)

        await self.refresh_token_repository.delete(hash_token(refresh_token))

        await self.refresh_token_repository.create(
            user_id=user_id,
            token=hash_token(new_refresh),
            expire_at=datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
        )

        await self.db.commit()

        return new_access, new_refresh
        
    async def logout(self, refresh_token: str):
        try:
            payload = decode_token(refresh_token)
            
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user_id = payload["sub"]
        
        await self.refresh_token_repository.delete(hash_token(refresh_token))
        await self.db.commit()
        
        logger.info(f"User logout. user_id={user_id}")