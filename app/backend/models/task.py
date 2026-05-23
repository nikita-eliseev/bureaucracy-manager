from datetime import date
from typing import Optional

from sqlalchemy import String, Date, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.backend.core.database import Base
from app.backend.core.task_enum import TaskStatus
from app.backend.models.user import User



class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    
    department_name: Mapped[str] = mapped_column(String(100)) 
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.draft)
    
    sent_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    deadline_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    user: Mapped["User"] = relationship(back_populates="tasks")