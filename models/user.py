# models/user.py
from datetime import datetime
from uuid import uuid4
import enum

from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.orm import relationship

from database import Base

class Role(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"

class User(Base):
    __tablename__ = "users"

    # store UUIDs as strings for SQLite simplicity
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    full_name = Column(String(255), nullable=True)
    role = Column(Enum(Role), nullable=False, default=Role.employee)

    # placeholder for hashing later
    password_hash = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relationship example if you link tasks: back_populates="assignee"
    # tasks = relationship("Task", back_populates="assignee")
