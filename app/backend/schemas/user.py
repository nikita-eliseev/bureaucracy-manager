from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=6,
        description="The password must be at least 6 characters long."
    )


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
    