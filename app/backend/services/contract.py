from datetime import date, timedelta

from fastapi import HTTPException, status

from app.backend.core.logger import logger
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
            monthly_price=payload.monthly_price,
            end_date=payload.end_date,
            cancellation_deadline=calculate_cancellation_deadline(
                end_date=payload.end_date, 
                notice_period_months=payload.notice_period_months
            ),
            notice_period_months=payload.notice_period_months
        )
        await self.db.commit()
        await self.db.refresh(contract)
        
        logger.info(
            f"Contract created. contract_id={contract.id}, user_id={user_id}"
        )
        
        return ContractResponse.model_validate(contract)
    
    async def update_contract(self, payload: ContractUpdate, user_id: str, contract_id: int):
        contract = await self.contract_repository.get_contract(user_id=user_id, contract_id=contract_id)

        if not contract:
            logger.warning(
                f"Contract not found. contract_id={contract_id}, user_id={user_id}"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Contract not found"
            )

        if payload.company is not None:
            contract.company = payload.company

        if payload.contract_type is not None:
            contract.contract_type = payload.contract_type
        
        if payload.monthly_price is not None:
            contract.monthly_price = payload.monthly_price

        if payload.notice_period_months is not None:
            contract.notice_period_months = payload.notice_period_months
        
        if payload.end_date is not None:
            contract.end_date = payload.end_date
            contract.cancellation_deadline = calculate_cancellation_deadline(contract.end_date, contract.notice_period_months)
        
        if payload.is_active is not None:
            contract.is_active = payload.is_active

        await self.db.commit()
        await self.db.refresh(contract)
        
        logger.info(
            f"Contract  updated. contract_id={contract_id}, user_id={user_id}"
        )
        
        return ContractResponse.model_validate(contract)
        
    async def delete_contract(self, user_id: str, contract_id: int) -> None:
        contract = await self.contract_repository.get_contract(user_id=user_id, contract_id=contract_id)
        if not contract:
            logger.warning(
                "Contract does not exist."
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This contract does not exist."
            )
        
        await self.contract_repository.delete_contract(contract=contract)
        await self.db.commit()
        
        logger.info(
            f"Contract  deleted. contract_id={contract_id}, user_id={user_id}"
        )
        
    async def get_all_contracts(self, user_id: str, limit: int, offset: int):
        contracts = await self.contract_repository.get_contracts(user_id=user_id, limit=limit, offset=offset)
        
        return contracts

    async def get_expiring_contracts(self, user_id: str, days: int = 30):
        today = date.today() 
        limit_date = today + timedelta(days=days)  
        
        result = await self.contract_repository.expire_contract(user_id=user_id, limit_date=limit_date)
        
        return result
    
    async def get_contract(self, user_id: str, contract_id: str):
        contract = await self.contract_repository.get_contract(user_id=user_id, contract_id=contract_id)  
        
        return contract
