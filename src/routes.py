from fastapi import APIRouter

from .users.controller import router as user
api_router = APIRouter()
api_router.include_router(user, prefix="/usres", tags=["Users/"])
