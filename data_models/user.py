from fastapi import APIRouter
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum

router = APIRouter()

class Role(str, Enum):
    admin = "admin"
    user = "user"

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    role: Role = Role.user

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[Role] = None
    password: Optional[str] = Field(None, min_length=6, max_length=100)

class UserOut(UserBase):
    id: UUID

