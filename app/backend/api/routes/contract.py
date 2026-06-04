from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse

from app.backend.core.dependencies import get_contract_serivece, get_current_user
from app.backend.schemas.contract import ContractCreate, ContractUpdate
from app.backend.services.contract import ContractService
from app.utils.pdf import generate_contract_pdf


router = APIRouter(prefix="/contracts", tags=["CONTRACTS"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def create(
    payload: ContractCreate,
    contract_services: ContractService = Depends(get_contract_serivece),  
    user_id: str = Depends(get_current_user)
):
    return await contract_services.create_contract(
        payload=payload, 
        user_id=user_id
    )
    
@router.patch("/{contract_id}", status_code=status.HTTP_200_OK)
async def update(
    contract_id: int,
    payload: ContractUpdate,
    user_id: str = Depends(get_current_user),
    contract_services: ContractService = Depends(get_contract_serivece)
):
    return await contract_services.update_contract(
        payload=payload,
        user_id=user_id,
        contract_id=contract_id
    )
    
@router.delete("/{contract_id}", status_code=status.HTTP_200_OK)
async def delete(
    contract_id: int,
    user_id: str = Depends(get_current_user),
    contract_services: ContractService = Depends(get_contract_serivece)
):
    await contract_services.delete_contract(user_id=user_id, contract_id=contract_id)
    return {
        "status": "Deleted"
    }
    
@router.get("", status_code=status.HTTP_200_OK)
async def all_contracts(
    user_id: str = Depends(get_current_user),
    contract_services: ContractService = Depends(get_contract_serivece)
):
    contracts = await contract_services.get_all_contracts(user_id=user_id)
    
    return [
        {
            "id": c.id,
            "company": c.company,
            "contract_type": c.contract_type,
            "end_date": c.end_date,
            "cancellation_deadline": c.cancellation_deadline,
        }
        for c in contracts
    ]
    
    
    
@router.get("/expiring", status_code=status.HTTP_200_OK)
async def get_expiring_contracts(
    days: int = Query(30, ge=1, le=365),
    user_id: str = Depends(get_current_user),
    contract_services: ContractService = Depends(get_contract_serivece)
):
    contracts = await contract_services.get_expiring_contracts(user_id=user_id, days=days)
    
    return [
        {
            "id": c.id,
            "company": c.company,
            "contract_type": c.contract_type,
            "end_date": c.end_date,
            "cancellation_deadline": c.cancellation_deadline,
        }
        for c in contracts
    ]
    
@router.get("/{contract_id}/pdf", status_code=status.HTTP_200_OK)
async def get_contract_pdf(
    contract_id: int, 
    user_id: str = Depends(get_current_user),
    contract_services: ContractService = Depends(get_contract_serivece)
):
    contract = await contract_services.get_contract(user_id=user_id, contract_id=contract_id)
    
    if not contract:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contract not found")
    
    pdf_buffer = generate_contract_pdf(contract=contract)
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="contract_{contract_id}.pdf"'
        }
    )
