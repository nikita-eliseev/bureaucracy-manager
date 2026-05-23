from typing import List

from app.backend.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from app.backend.models.contract import Contract
from app.backend.models.task import Task

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    contracts: Mapped[List["Contract"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    tasks: Mapped[List["Task"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )