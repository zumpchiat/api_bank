from datetime import datetime

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.contrib.models import BaseModel

class UserModel(BaseModel):
    __tablename__ = 'users'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(25), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)