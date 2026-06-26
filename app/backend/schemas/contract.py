from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict, field_validator


class ContractCreate(BaseModel):
    company: str = Field(
        ..., 
        min_length=2, 
        max_length=100, 
        examples=["Vodafone", "TK Krankenkasse"]
    )
    company_address: str = Field(
        ...,
        min_length=5,
        max_length=100
    )
    contract_type: str
    monthly_price: Decimal = Field(gt=0)
    end_date: date
    notice_period_months: int = Field(default=1, ge=1, le=12, description="Notice period in months, usually 1 or 3")
    
    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, value: date):
        if value < date.today():
            raise ValueError("end_date must be today or in the future")
        return value
    
    

class ContractUpdate(BaseModel):
    company: str | None = None
    company_address: str | None = None
    contract_type: str | None = None
    monthly_price: Decimal | None = None
    end_date: date | None = None
    notice_period_months: int | None = Field(default=1, ge=1, le=12, description="Notice period in months, usually 1 or 3")
    is_active: bool | None = None

class ContractResponse(BaseModel):
    id: int
    company: str
    company_address: str
    contract_type: str
    monthly_price: Decimal
    end_date: date
    cancellation_deadline: date
    is_active: bool
    notice_period_months: int

    model_config = ConfigDict(from_attributes=True)