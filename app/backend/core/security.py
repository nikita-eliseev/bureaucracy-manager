from datetime import datetime, timedelta, timezone
import hashlib
import uuid
from jose import jwt
from passlib.context import CryptContext
from app.backend.core.config import settings


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_token(user_id: str):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),  
        "type": "access"        
    }
    
    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm 
    )
    
def create_refresh_token(user_id: str):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + timedelta(days=settings.refresh_token_expire_days),
        "jti": str(uuid.uuid4()),
        "type": "refresh"
    }
    
    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm 
    )
    
def decode_token(token: str):
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm] 
    )
    
def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()