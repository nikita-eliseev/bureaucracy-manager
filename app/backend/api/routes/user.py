from fastapi import APIRouter, Depends, status

from app.backend.core.dependencies import get_current_user, get_user_service
from app.backend.schemas.user import UserProfileUpdate
from app.backend.services.user import UserService


router = APIRouter(tags=["USER"])

@router.patch("/user", status_code=status.HTTP_200_OK)
async def user_update(
    payload: UserProfileUpdate,
    user_id: str = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.update_user(user_id=user_id, payload=payload)