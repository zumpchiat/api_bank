from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, status, Body,HTTPException
from sqlalchemy.future import select

from src.contrib.dependecies import DatabaseDependency
from src.users.schemas import UserIn, UserOut

from src.users.models import UserModel
router = APIRouter()

@router.get(path="/")
async def get_all():
    pass


@router.post(path="/", summary="Create users", status_code=status.HTTP_201_CREATED)
async def create(
        db_session: DatabaseDependency,
        userIn:UserIn = Body(...) ) -> UserOut:

    user_nome = userIn.nome
    user_email = userIn.email
    user_password = userIn.password

    user = ((await db_session.execute(
            select(UserModel)
            .filter_by(email = user_email)))
            .scalars()
            .first())

    if user:
        raise HTTPException(
            status_code = status.HTTP_303_SEE_OTHER,
            detail = f"Email  {user_email} existente"
        )

    try:
        user_model = UserModel(
            id=uuid4(),
            created_at=datetime.now(),
            nome=userIn.nome,
            email=userIn.email,
            password=userIn.password  # Lembre-se de hash/criptografar a senha na vida real!
        )
        db_session.add(user_model)

        await db_session.commit()


    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Erro interno ao salvar User ",
        )

    return user_model