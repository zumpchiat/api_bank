from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.auth.services import decode_access_token, get_user_by_id

# Importe o serviço de usuário (User Service) para buscar o usuário no DB
# from views.user import UserOut  # Supondo que você tenha um modelo de usuário de saída

# Define o esquema de segurança. O token será esperado no header 'Authorization: Bearer <token>'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Decodifica o token, verifica a validade e retorna o objeto do usuário."""

    # 1. Decodifica e valida o token
    token_data = decode_access_token(token)

    # 2. Extrai a identidade do usuário
    user_id = token_data.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Busca o usuário completo no banco (melhor prática para garantir que o usuário existe e está ativo)
    # user = await user_service.get_user_by_id(user_id)
    user = await get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário do token não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 4. Retorna o objeto do usuário (o objeto PostOut ou UserOut)
    return user