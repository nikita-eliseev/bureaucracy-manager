from fastapi import APIRouter, Depends, status

from app.backend.core.dependencies import get_contract_serivece, get_current_user
from app.backend.schemas.contract import ContractCreate, ContractUpdate
from app.backend.services.contract import ContractService


router = APIRouter(prefix="/contracts", tags=["CONTRACTS"])

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create(
    payload: ContractCreate,
    contract_services: ContractService = Depends(get_contract_serivece),  
    user_id: str = Depends(get_current_user)
):
    return await contract_services.create_contract(
        payload=payload, 
        user_id=user_id
    )
    
@router.patch("/update/{contract_id}", status_code=status.HTTP_200_OK)
async def update(
    contract_id: int,
    payload: ContractUpdate,
    contract_services: ContractService = Depends(get_contract_serivece)
):
    return await contract_services.update_contract(
        payload=payload,
        contract_id=contract_id
    )
    
@router.delete("/delete/{contract_id}", status_code=status.HTTP_200_OK)
async def delete(
    contract_id: int,
    contract_services: ContractService = Depends(get_contract_serivece)
):
    await contract_services.delete_contract(contract_id=contract_id)
    return {
        "status": "Deleted"
    }