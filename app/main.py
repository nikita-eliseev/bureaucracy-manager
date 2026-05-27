from fastapi import FastAPI
from app.backend.core.config import settings
import app.backend.models
from app.backend.api.routes.auth import router as auth_router

app = FastAPI(
    title="BEREAUCRACY-MANAGER",
    debug=settings.debug
)

app.include_router(auth_router)