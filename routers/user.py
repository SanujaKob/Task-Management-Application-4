# routers/user.py
from typing import List, Dict
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, Response, status

from data_models.user import EmployeeCreate, EmployeeOut, EmployeeUpdate

router = APIRouter()

# In-memory "DB" for employees (module-level)
employees_db: Dict[UUID, dict] = {}


@router.post("", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeCreate):
    """
    Create an employee. Server generates UUID.
    """
    new_id = uuid4()
    record = payload.model_dump()
    record["id"] = new_id
    employees_db[new_id] = record
    return EmployeeOut(**record)


@router.get("", response_model=List[EmployeeOut])
def list_employees():
    return [EmployeeOut(**e) for e in employees_db.values()]


@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: UUID):
    emp = employees_db.get(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return EmployeeOut(**emp)


@router.patch("/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: UUID, payload: EmployeeUpdate):
    emp = employees_db.get(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    update_data = payload.model_dump(exclude_unset=True)
    emp.update(update_data)
    employees_db[employee_id] = emp
    return EmployeeOut(**emp)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: UUID):
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    del employees_db[employee_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
