from datetime import datetime
from typing import List
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.backend.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.backend.models.contract import Contract


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    contracts: Mapped[List["Contract"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )