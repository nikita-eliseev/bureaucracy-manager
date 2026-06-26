from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse

from app.backend.core.dependencies import get_contract_service, get_current_user, get_user_service
from app.backend.schemas.contract import ContractCreate, ContractResponse, ContractUpdate
from app.backend.services.contract import ContractService
from app.backend.services.user import UserService
from app.utils.pdf import generate_cancellation_letter_pdf


router = APIRouter(prefix="/contracts", tags=["CONTRACTS"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ContractResponse)
async def create(
    payload: ContractCreate,
    contract_services: ContractService = Depends(get_contract_service),  
    user_id: str = Depends(get_current_user)
):
    return await contract_services.create_contract(
        payload=payload, 
        user_id=user_id
    )
    
@router.patch("/{contract_id:int}", status_code=status.HTTP_200_OK, response_model=ContractResponse)
async def update(
    contract_id: int,
    payload: ContractUpdate,
    user_id: str = Depends(get_current_user),
    contract_services: ContractService = Depends(get_contract_service)
):
    return await contract_services.update_contract(
        payload=payload,
        user_id=user_id,
        contract_id=contract_id
    )
    
@router.delete("/{contract_id:int}", status_code=status.HTTP_200_OK)
async def delete(
    contract_id: int,
    user_id: str = Depends(get_current_user),
    contract_services: ContractService = Depends(get_contract_service)
):
    await contract_services.delete_contract(user_id=user_id, contract_id=contract_id)
    return {
        "status": "Deleted"
    }
    
@router.get(
    "/{contract_id:int}", 
    status_code=status.HTTP_200_OK, 
    response_model=ContractResponse
)
async def get_contract(
    contract_id: int,
    user_id: str = Depends(get_current_user),
    contract_services: ContractService = Depends(get_contract_service)
):
    contract = await contract_services.get_contract(user_id=user_id, contract_id=contract_id)
    
    if not contract:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contract not found")
    
    return ContractResponse.model_validate(contract)
    
@router.get(
    "", 
    status_code=status.HTTP_200_OK, 
    response_model=list[ContractResponse]
)
async def all_contracts(
    user_id: str = Depends(get_current_user),
    contract_services: ContractService = Depends(get_contract_service),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    contracts = await contract_services.get_all_contracts(user_id, limit, offset)
    
    return [ContractResponse.model_validate(c) for c in contracts]
    
    

@router.get(
    "/expiring", 
    status_code=status.HTTP_200_OK, 
    response_model=list[ContractResponse]
)
async def get_expiring_contracts(
    days: int = Query(30, ge=1, le=365),
    user_id: str = Depends(get_current_user),
    contract_services: ContractService = Depends(get_contract_service)
):
    contracts = await contract_services.get_expiring_contracts(user_id=user_id, days=days)
    
    return [ContractResponse.model_validate(c) for c in contracts]
    
@router.get("/{contract_id:int}/pdf", status_code=status.HTTP_200_OK)
async def get_contract_pdf(
    contract_id: int, 
    user_id: str = Depends(get_current_user),
    contract_services: ContractService = Depends(get_contract_service),
    user_services: UserService = Depends(get_user_service)
):
    contract = await contract_services.get_contract(user_id=user_id, contract_id=contract_id)
    
    if not contract:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contract not found")
    
    user = await user_services.get_user(user_id=user_id)
    
    pdf_buffer = generate_cancellation_letter_pdf(contract=contract, user=user)
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="contract_{contract_id}.pdf"'
        }
    )
