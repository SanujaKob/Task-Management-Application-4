# models/task.py
from __future__ import annotations

from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
from uuid import UUID
import enum

# --- SQLAlchemy ---
from sqlalchemy import Column, String, Integer, Enum as SAEnum, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from database import Base  # adjust import path if needed

if TYPE_CHECKING:
    from models.user import User

# ==========================
# Enums (shared DB & API)
# ==========================
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
    re_submit = "re_submit"  # distinct from 'rejected'

# ==========================
# SQLAlchemy Database Model
# ==========================
class Task(Base):
    __tablename__ = "tasks"

    # You said: "UUID from client" → no default here
    id = Column(String(36), primary_key=True, index=True)

    title = Column(String(200), nullable=False, index=True)
    description = Column(String, nullable=True)

    priority = Column(SAEnum(Priority), nullable=False, default=Priority.low)
    status   = Column(SAEnum(Status),   nullable=False, default=Status.not_started)
    progress = Column(Integer, nullable=False, default=0)  # 0..100

    due_date = Column(Date, nullable=True)

    # --- Linkage to User (assignee) ---
    # FK ensures assignee_id references users.id.
    # ondelete="SET NULL" lets you delete a user without deleting tasks (task becomes unassigned).
    assignee_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    assignee: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="tasks",
        lazy="joined",
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

# ==========================
# Pydantic Schemas (v2)
# ==========================
from pydantic import BaseModel, Field, ConfigDict

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Priority = Priority.low
    status: Status = Status.not_started
    progress: int = Field(0, ge=0, le=100)
    due_date: Optional[date] = None
    assignee_id: Optional[str] = None  # UUID string of a User
    model_config = ConfigDict(from_attributes=True)

class TaskIdMixin(BaseModel):
    # Client supplies this (no default) to match your DB choice
    id: UUID
    model_config = ConfigDict(from_attributes=True)

class TaskCreate(TaskIdMixin, TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[Status] = None
    progress: Optional[int] = Field(None, ge=0, le=100)
    due_date: Optional[date] = None
    assignee_id: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class TaskOut(TaskIdMixin, TaskBase):
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

__all__ = [
    "Priority", "Status",
    "Task",
    "TaskBase", "TaskCreate", "TaskUpdate", "TaskOut",
]
