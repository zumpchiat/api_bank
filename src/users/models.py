from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.contrib.models import BaseModel

class User(BaseModel):
    __table__ = 'users'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)