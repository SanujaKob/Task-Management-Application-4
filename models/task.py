# models/task.py
from __future__ import annotations

from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
import enum
import uuid

from sqlalchemy import Column, String, Integer, Enum as SAEnum, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from database import Base

if TYPE_CHECKING:
    from models.user import User

# ----- Enums -----
class Priority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class Status(str, enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"
    approved = "approved"
    rejected = "rejected"
    re_submit = "re_submit"

def generate_short_id() -> str:
    return uuid.uuid4().hex[:5]

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(5), primary_key=True, index=True, default=generate_short_id)

    assignee_id = Column(
        String(5),  # must match users.id length
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    title = Column(String(200), nullable=False, index=True)
    description = Column(String, nullable=True)

    priority = Column(SAEnum(Priority), nullable=False, default=Priority.low)
    status   = Column(SAEnum(Status),   nullable=False, default=Status.not_started)
    progress = Column(Integer, nullable=False, default=0)

    due_date = Column(Date, nullable=True)

    assignee: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="tasks",
        lazy="joined",
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

# ----- Pydantic Schemas (v2) -----
from pydantic import BaseModel, Field, ConfigDict

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Priority = Priority.low
    status: Status = Status.not_started
    progress: int = Field(0, ge=0, le=100)
    due_date: Optional[date] = None
    assignee_id: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class TaskCreate(TaskBase):
    pass  # id is auto-generated

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[Status] = None
    progress: Optional[int] = Field(None, ge=0, le=100)
    due_date: Optional[date] = None
    assignee_id: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class TaskOut(TaskBase):
    id: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

__all__ = [
    "Priority", "Status",
    "Task",
    "TaskBase", "TaskCreate", "TaskUpdate", "TaskOut",
]
