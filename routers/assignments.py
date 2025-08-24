# routers/assignments.py
from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from database import get_db
from models.task import Task as TaskModel, TaskOut
from models.user import User, Role

# NOTE: no prefix/tags here — your main.py adds prefix="/assignments", tags=["Assignments"]
router = APIRouter()

# --- Request body model (Pydantic) ---
class AssignBody(BaseModel):
    assignee_id: UUID
    model_config = ConfigDict(from_attributes=True)

@router.post("/tasks/{task_id}/assign", response_model=TaskOut)
def assign_task(
    task_id: UUID,
    body: AssignBody,
    db: Session = Depends(get_db),
):
    task = db.get(TaskModel, str(task_id))
    if not task:
        raise HTTPException(404, "Task not found")

    user = db.get(User, str(body.assignee_id))
    if not user:
        raise HTTPException(404, "Assignee not found")

    if user.role not in (Role.employee, Role.manager):
        raise HTTPException(400, "Assignee must be an employee or manager")

    task.assignee_id = str(body.assignee_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.post("/tasks/{task_id}/unassign", response_model=TaskOut)
def unassign_task(
    task_id: UUID,
    db: Session = Depends(get_db),
):
    task = db.get(TaskModel, str(task_id))
    if not task:
        raise HTTPException(404, "Task not found")

    task.assignee_id = None
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/employees/{employee_id}/tasks", response_model=List[TaskOut])
def tasks_for_employee(
    employee_id: UUID,
    db: Session = Depends(get_db),
):
    user = db.get(User, str(employee_id))
    if not user:
        raise HTTPException(404, "Employee not found")

    results = (
        db.query(TaskModel)
        .filter(TaskModel.assignee_id == str(employee_id))
        .all()
    )
    return results

# Back-compat alias (so either import style works)
assignments_router = router
