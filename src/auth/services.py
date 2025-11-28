from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

import bcrypt
from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.future import select

from src.configs.settings import settings
from src.contrib.dependecies import DatabaseDependency
from src.users.models import UserModel


# ---------------- Funções de Senha ----------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


# Define o algoritmo de hash para senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------- Funções de JWT ----------------


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria um Access Token JWT com payload e expiração."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Padrão: usa o tempo definido em settings
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    # Assina o token usando a chave secreta e o algoritmo
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """Decodifica e valida o Access Token."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # Você pode adicionar validações de payload aqui (e.g., verificar se 'user_id' existe)
        return payload
    except JWTError as e:
        # Levanta exceção se o token for inválido, expirado, ou a assinatura falhar.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas ou token expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Simula a busca de um usuário pelo username
async def get_user_by_username(username: str, db_session: DatabaseDependency) -> Optional[Dict]:
    """Busca um usuário na lista hardcoded pelo username."""

    user = ((await db_session.execute(select(UserModel).where(nome=username))).scalars().first())
    if user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not Found"
        )

    return user


# Simula a busca de um usuário pelo ID (usado após decodificar o JWT)
async def get_user_by_id(user_id: str, db_session: DatabaseDependency) -> Optional[Dict]:
    """Busca um usuário no banco de dados pelo ID."""

    user = ((await db_session.execute(select(UserModel).where(id=user_id))).scalars().first())

    return user
