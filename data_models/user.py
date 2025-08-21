from fastapi import APIRouter
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from uuid import UUID
from enum import Enum

router = APIRouter()

# ---- Roles ----
class Role(str, Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"   # renamed from "user"

# ---- Base (shared fields) ----
class EmployeeBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    role: Role = Role.employee   # default role is employee

# ---- For POST /employees ----
class EmployeeCreate(EmployeeBase):
    password: str = Field(..., min_length=6, max_length=100)

# ---- For PATCH/PUT /employees/{id} ----
class EmployeeUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[Role] = None
    password: Optional[str] = Field(None, min_length=6, max_length=100)

# ---- What you send back ----
class EmployeeOut(EmployeeBase):
    id: UUID
