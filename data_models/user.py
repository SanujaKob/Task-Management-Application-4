# data_models/user.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from uuid import UUID
from pydantic import ConfigDict
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"

class EmployeeBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    role: Role = Role.employee

class EmployeeCreate(EmployeeBase):
    password: str = Field(..., min_length=6, max_length=100)

class EmployeeUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[Role] = None
    password: Optional[str] = Field(None, min_length=6, max_length=100)

class EmployeeOut(EmployeeBase):
    id: UUID

    # Pydantic v2: allow from ORM objects (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)
