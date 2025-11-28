from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm  # Necessário para o fluxo OAuth2

from src.configs.settings import settings
from src.auth.schemas import LoginData, Token
from src.auth.services  import (
    create_access_token,
    get_user_by_id,
    get_user_by_username,
    verify_password,
)

# Importe o serviço de usuário (User Service) para buscar o usuário no DB

router = APIRouter()


@router.post("/login", response_model=Token)
# OAuth2PasswordRequestForm recebe username e password como form data
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    # 1. Busca o usuário no DB pelo username (ASSUMIMOS O SERVIÇO DE USUÁRIO)
    # user_in_db = await user_service.get_user_by_username(form_data.username)
    user_in_db = await get_user_by_username(form_data.username)

    if not user_in_db or not verify_password(
        form_data.password, user_in_db["password"]
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        # 2. Credenciais válidas: gera o token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user_in_db["nome"], "user_id": user_in_db["id"]},
        expires_delta=access_token_expires,
    )

    # 3. Retorna o token para o cliente
    return {"access_token": access_token, "token_type": "bearer"}