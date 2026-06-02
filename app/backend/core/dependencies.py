from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.core.database import AsyncSessionLocal
from app.backend.core.security import decode_token
from app.backend.services.auth import AuthService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.backend.services.contract import ContractService

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    
    try:
        payload = decode_token(token=token)

        if payload.get("type") != "access":
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
            
        return user_id
    
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
        


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        
async def get_auth_serivece(db: AsyncSession = Depends(get_db)):
    return AuthService(db=db)

async def get_contract_serivece(db: AsyncSession = Depends(get_db)):
    return ContractService(db=db)