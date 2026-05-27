from fastapi import FastAPI
from core.config import settings
import models
from api.routes.auth import router as auth_router
app = FastAPI(
    title="BEREAUCRACY-MANAGER",
    debug=settings.debug
)

app.include_router(auth_router)