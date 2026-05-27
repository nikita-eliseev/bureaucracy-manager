from fastapi import APIRouter, Depends, HTTPException
from fastapi import status

from app.backend.core.dependencies import get_auth_serivece
from app.backend.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse
from app.backend.services.auth import AuthService

router = APIRouter(default="auth", tags=["AUTH"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest, 
    auth_service: AuthService = Depends(get_auth_serivece)
):
    return await auth_service.register(
        email=payload.email, 
        password=payload.password
    )

@router.post("/login")
async def login(
    payload: LoginRequest, 
    auth_service: AuthService = Depends(get_auth_serivece)
):

    tokens = await auth_service.login(
        payload.email, 
        payload.password
    )

    if not tokens:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access, refresh = tokens

    return TokenResponse(
        access_token=access,
        refresh_token=refresh
    )

@router.post("/refresh")
async def refresh(
    paylaod: RefreshRequest, 
    auth_service: AuthService = Depends(get_auth_serivece)
):
    token = await auth_service.refresh(paylaod.refresh_token)

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return {"access_token": token}

@router.post("/logout")
async def logout(
    payload: RefreshRequest, 
    auth_service: AuthService = Depends(get_auth_serivece)
):

    await auth_service.logout(payload.refresh_token)

    return {"status": "ok"}