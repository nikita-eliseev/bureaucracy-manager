from fastapi import HTTPException, status

from app.backend.core.config import calculate_cancellation_deadline
from app.backend.repositories.contract import ContractRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.schemas.contract import ContractCreate, ContractResponse, ContractUpdate

class ContractService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.contract_repository = ContractRepository(db=db)
        
        
    async def create_contract(self, payload: ContractCreate, user_id: str) -> ContractResponse:
        contract = await self.contract_repository.create(
            user_id=user_id,
            company=payload.company,
            contract_type=payload.contract_type,
            end_date=payload.end_date,
            cancellation_deadline=calculate_cancellation_deadline(
                end_date=payload.end_date, 
                notice_period_months=payload.notice_period_months
            ),
            notice_period_months=payload.notice_period_months
        )
        
        await self.db.commit()
        await self.db.refresh(contract)
        
        return ContractResponse.model_validate(contract)
    
    async def update_contract(self, payload: ContractUpdate, contract_id: int):
        contract = await self.contract_repository.get_contract_by_id(contract_id)

        if not contract:
            raise HTTPException(404, "Not found")

        if payload.company is not None:
            contract.company = payload.company

        if payload.contract_type is not None:
            contract.contract_type = payload.contract_type

        if payload.notice_period_months is not None:
            contract.notice_period_months = payload.notice_period_months
        
        if payload.end_date is not None:
            contract.end_date = payload.end_date
            contract.cancellation_deadline = calculate_cancellation_deadline(contract.end_date, contract.notice_period_months)
        
        if payload.is_active is not None:
            contract.is_active = payload.is_active

        await self.db.commit()
        await self.db.refresh(contract)

        return ContractResponse.model_validate(contract)
        
    async def delete_contract(self, contract_id: int) -> None:
        contract = await self.contract_repository.get_contract_by_id(contract_id=contract_id)
        if not contract:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This contract does not exist."
            )
        
        await self.contract_repository.delete_contract(contract=contract)
        await self.db.commit()