# models/task.py
from datetime import datetime, date
from uuid import uuid4
import enum

from sqlalchemy import Column, String, Integer, Enum, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

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
    rejected = "re_submit"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True)  # UUID from client
    title = Column(String(200), nullable=False, index=True)
    description = Column(String, nullable=True)
    priority = Column(Enum(Priority), nullable=False, default=Priority.low)
    status = Column(Enum(Status), nullable=False, default=Status.not_started)
    progress = Column(Integer, nullable=False, default=0)
    due_date = Column(Date, nullable=True)

    assignee_id = Column(String, ForeignKey("employees.id"), nullable=True)
    assignee = relationship("Employee", back_populates="tasks")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
