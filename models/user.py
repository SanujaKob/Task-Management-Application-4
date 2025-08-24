# models/user.py
from __future__ import annotations
from database import Base
from datetime import datetime
from uuid import uuid4, UUID
import enum
from typing import Optional

# --- SQLAlchemy imports ---
from sqlalchemy import Column, String, Enum as SAEnum, DateTime
from sqlalchemy.orm import relationship

# Adjust this import path if your Base is elsewhere
from database import Base

# ==========================
# Enums (shared by DB & API)
# ==========================
class Role(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"


# ==========================
# SQLAlchemy Database Model
# ==========================
class User(Base):
    __tablename__ = "users"

    # store UUIDs as strings for SQLite simplicity
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()), index=True)

    username   = Column(String(50),  nullable=False, unique=True, index=True)
    email      = Column(String(255), nullable=False, unique=True, index=True)
    full_name  = Column(String(255), nullable=True)
    role       = Column(SAEnum(Role), nullable=False, default=Role.employee)

    # placeholder for hashing later
    password_hash = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # If you link tasks later:
    # tasks = relationship("Task", back_populates="assignee")


# ==========================
# Pydantic Schemas (v2)
# ==========================
from pydantic import BaseModel, Field, EmailStr, ConfigDict

class EmployeeBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    role: Role = Role.employee

    # Allow building from ORM objects (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)

class EmployeeCreate(EmployeeBase):
    password: str = Field(..., min_length=6, max_length=100)

class EmployeeUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[Role] = None
    password: Optional[str] = Field(None, min_length=6, max_length=100)

    model_config = ConfigDict(from_attributes=True)

class EmployeeOut(EmployeeBase):
    # DB stores id as str(UUID), but Pydantic will coerce to UUID on output
    id: UUID

    model_config = ConfigDict(from_attributes=True)


# Optional: convenient exports
__all__ = [
    "Role",
    "User",
    "EmployeeBase",
    "EmployeeCreate",
    "EmployeeUpdate",
    "EmployeeOut",
]
