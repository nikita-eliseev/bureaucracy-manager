from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UserResponse(BaseModel):
    email: EmailStr
    full_name: str | None = None
    address: str | None = None
    city: str | None = None
    postal_code: str | None = None
    country: str | None = None
    
    model_config = ConfigDict(from_attributes=True)


    
class UserProfileUpdate(BaseModel):
    email: EmailStr | None = None
    
    full_name: str | None = None
    
    address: str | None = None
    
    city: str | None = None
    
    postal_code: str | None = None
    
    country: str | None = None
    
    
    