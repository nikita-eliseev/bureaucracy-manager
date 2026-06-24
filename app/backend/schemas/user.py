from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


# class UserResponse(BaseModel):
#     id: int
#     email: EmailStr
#     is_active: bool
#     created_at: datetime

#     model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    email: EmailStr
    full_name: str
    address: str
    city: str
    postal_code: str
    country: str
    
    model_config = ConfigDict(from_attributes=True)


    
class UserProfileUpdate(BaseModel):
    email: EmailStr | None = None
    
    full_name: str | None = None
    
    address: str | None = None
    
    city: str | None = None
    
    postal_code: str | None = None
    
    country: str | None = None
    
    
    