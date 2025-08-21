# routers/user.py
from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.user import User, Role
from data_models.user import EmployeeCreate, EmployeeUpdate, EmployeeOut

router = APIRouter()

def to_employee_out(u: User) -> EmployeeOut:
    return EmployeeOut.model_validate(u)  # uses from_attributes=True

@router.post("", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    # uniqueness checks (simple)
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        username=payload.username,
        email=payload.email,
        full_name=payload.full_name,
        role=Role(payload.role),
        # TODO: hash password; storing plaintext is insecure
        password_hash=payload.password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return to_employee_out(user)

@router.get("", response_model=List[EmployeeOut])
def list_employees(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [to_employee_out(u) for u in users]

@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == str(employee_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Employee not found")
    return to_employee_out(user)

@router.patch("/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: UUID, payload: EmployeeUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == str(employee_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Employee not found")

    data = payload.model_dump(exclude_unset=True)

    # handle username/email uniqueness if they’re changing
    if "username" in data:
        exists = db.query(User).filter(User.username == data["username"], User.id != user.id).first()
        if exists:
            raise HTTPException(status_code=400, detail="Username already exists")
        user.username = data["username"]

    if "email" in data:
        exists = db.query(User).filter(User.email == data["email"], User.id != user.id).first()
        if exists:
            raise HTTPException(status_code=400, detail="Email already exists")
        user.email = data["email"]

    if "full_name" in data:
        user.full_name = data["full_name"]
    if "role" in data and data["role"] is not None:
        user.role = Role(data["role"])
    if "password" in data and data["password"] is not None:
        # TODO: hash password
        user.password_hash = data["password"]

    db.commit()
    db.refresh(user)
    return to_employee_out(user)

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == str(employee_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(user)
    db.commit()
    return None
