from datetime import date
from pydantic import BaseModel, Field, ConfigDict


class ContractCreate(BaseModel):
    company: str = Field(
        ..., 
        min_length=2, 
        max_length=100, 
        examples=["Vodafone", "TK Krankenkasse"]
    )
    contract_type: str
    end_date: date
    notice_period_months: int = Field(default=1, ge=1, le=12, description="Notice period in months, usually 1 or 3")
    

class ContractUpdate(BaseModel):
    company: str | None = None
    contract_type: str | None = None
    end_date: date | None = None
    notice_period_months: int | None = None
    is_active: bool | None = None

class ContractResponse(BaseModel):
    id: int
    company: str
    contract_type: str
    end_date: date
    cancellation_deadline: date
    is_active: bool
    notice_period_months: int

    model_config = ConfigDict(from_attributes=True)