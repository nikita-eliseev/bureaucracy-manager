from fastapi import HTTPException,status

from app.backend.core.logger import logger
from app.backend.core.database import AsyncSession
from app.backend.repositories.user import UserRepository
from app.backend.schemas.user import UserProfileUpdate, UserResponse


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UserRepository(db=db)
        
    async def update_user(self, user_id: str, payload: UserProfileUpdate) -> UserResponse:
        user = await self.user_repository.get_by_id(user_id=user_id)
        
        if not user:
            logger.warning(f"User does not found. user_id={user_id}")
            
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User does not found."
            )
        
        if payload.email is not None:
            user.email = payload.email
            
        if payload.full_name is not None:
            user.full_name = payload.full_name
            
        if payload.address is not None:
            user.address = payload.address
            
        if payload.city is not None:
            user.city = payload.city
            
        if payload.postal_code is not None:
            user.postal_code = payload.postal_code
            
        if payload.country is not None:
            user.country = payload.country
            
        await self.db.commit()
        await self.db.refresh(user)
        
        logger.info(f"User updated. user_id={user_id}")
        
        return UserResponse.model_validate(user)
    
    async def get_user(self, user_id: str) -> UserResponse:
        user = await self.user_repository.get_by_id(user_id=user_id)
        
        if not user:
            logger.warning(f"User does not found. user_id={user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                                detail="User does not found"
                            )
            
        return UserResponse.model_validate(user)