from datetime import date
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.backend.models.contract import Contract


class ContractRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        
    async def create(
        self, 
        user_id: str,
        company: str, 
        contract_type: str,
        monthly_price: Decimal,
        cancellation_deadline: date,
        end_date: date,
        notice_period_months: int
    ) -> Contract:
        contract = Contract(
            user_id=user_id,
            company=company,
            contract_type=contract_type,
            monthly_price=monthly_price,
            end_date=end_date,
            cancellation_deadline=cancellation_deadline,
            notice_period_months=notice_period_months
        )
        self.db.add(contract)
        
        return contract
        
    async def delete_contract(self, contract: Contract) -> None:
        await self.db.delete(contract)
      
    async def get_contracts(self, user_id: str, limit: int, offset: int):
        result = await self.db.execute(
            select(Contract)
            .where(Contract.user_id == user_id)
            .limit(limit=limit)
            .offset(offset=offset)
        )
        
        return result.scalars().all()
    
    
    async def expire_contract(self, user_id: str, limit_date: date):
        result = await self.db.execute(
            select(Contract).where(
                Contract.user_id == user_id,
                Contract.is_active == True,
                Contract.cancellation_deadline <= limit_date 
            )
        )
        
        return result.scalars().all()
    
    async def get_contract(self, user_id: str, contract_id: str) -> Contract:
        result = await self.db.execute(
            select(Contract).where(
                Contract.user_id == user_id,
                Contract.id == contract_id
            )
        )
        
        return result.scalar_one_or_none()
        