from typing import Annotated

from pydantic import Field, BaseModel


class User(BaseModel):
    nome: Annotated[str, Field(description="Nome do user", examples="João", max_length=50)]
    email: Annotated[str, Field(description="Email do user", examples="email@email.com", max_length=60)]