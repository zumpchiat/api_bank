from typing import Annotated

from pydantic import Field, BaseModel

from src.contrib.schemas import OutMixin


class User(BaseModel):

    nome: Annotated[str, Field(description="Nome do user", examples=["João"], max_length=50)]
    email: Annotated[str, Field(description="Email do user", examples=["email@email.com"], max_length=60)]
    password: Annotated[str, Field(description="Senha do users", max_length=25)]


class UserIn(User):
    pass


class UserOut(User, OutMixin):
    pass


