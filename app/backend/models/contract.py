from datetime import date, datetime
from sqlalchemy import String, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.backend.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.backend.models.user import User


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
        nullable=False,
    )

    company: Mapped[str] = mapped_column(String(255), nullable=False)
    contract_type: Mapped[str] = mapped_column(String(100), nullable=False)

    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    cancellation_deadline: Mapped[date] = mapped_column(Date, nullable=False)

    notice_period_months: Mapped[int] = mapped_column(default=3)

    is_active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    user: Mapped["User"] = relationship(back_populates="contracts")