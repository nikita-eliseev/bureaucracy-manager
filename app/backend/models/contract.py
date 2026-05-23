from datetime import date

from app.backend.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Date, ForeignKey, Integer, String

from app.backend.models.user import User


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    
    service_name: Mapped[str] = mapped_column(String(100)) 
    end_date: Mapped[date] = mapped_column(Date)

    notice_period_months: Mapped[int] = mapped_column(Integer, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["User"] = relationship(back_populates="contracts")