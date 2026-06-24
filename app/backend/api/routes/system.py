from fastapi import APIRouter


router = APIRouter(tags=["SYSTEM"])

@router.get("/health")
async def health():
    return {
        "status": "ok"
    }
