from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.backend.models.contract import Contract


class ContractRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    async def get_contract_by_id(self, contract_id: int) -> Contract | None:
        contract = await self.db.execute(
            select(Contract).where(Contract.id == contract_id)
        )
        return contract.scalar_one_or_none()
        
    async def create(
        self, 
        user_id: str,
        company: str, 
        contract_type: str,
        cancellation_deadline: date,
        end_date: date,
        notice_period_months: int
    ) -> Contract:
        contract = Contract(
            user_id=user_id,
            company=company,
            contract_type=contract_type,
            end_date=end_date,
            cancellation_deadline=cancellation_deadline,
            notice_period_months=notice_period_months
        )
        self.db.add(contract)
        
        return contract
        
    async def delete_contract(self, contract: Contract) -> None:
        await self.db.delete(contract)
        
        