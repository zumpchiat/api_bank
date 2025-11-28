from fastapi import APIRouter

from .users.controller import router as user
from src.auth.controller import router as auth

api_router = APIRouter()
api_router.include_router(user, prefix="/users", tags=["Users/"])
api_router.include_router(auth, prefix="/auth", tags=["Autenticação"])
