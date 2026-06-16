from fastapi import FastAPI
from app.backend.core.config import settings
from app.backend.api.routes.auth import router as auth_router
from app.backend.api.routes.contract import router as document_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="BEREAUCRACY-MANAGER",
    debug=settings.debug,
    root_path="/api"
)


app.include_router(auth_router)
app.include_router(document_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

