# routers/task.py
from typing import List, Dict
from datetime import datetime

from fastapi import APIRouter, HTTPException, Response, status

from models.task import TaskCreate, TaskOut, TaskUpdate, generate_short_id

router = APIRouter()

# In-memory "DB" for tasks (module-level)
tasks_db: Dict[str, TaskOut] = {}


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    """
    Create a task. ID is auto-generated (5-char short ID).
    """
    new_id = generate_short_id()
    if new_id in tasks_db:
        # Extremely unlikely with 5 chars, but guard anyway
        raise HTTPException(status_code=409, detail="Generated ID collision, try again")

    now = datetime.utcnow()
    new_task = TaskOut(
        id=new_id,
        created_at=now,
        updated_at=now,
        **payload.model_dump(),
    )
    tasks_db[new_id] = new_task
    return new_task


@router.get("", response_model=List[TaskOut])
def list_tasks():
    return list(tasks_db.values())


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: str):
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: str, payload: TaskUpdate):
    existing = tasks_db.get(task_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_data = payload.model_dump(exclude_unset=True)
    updated_task = existing.model_copy(update=updated_data)
    # bump updated_at
    updated_task = updated_task.model_copy(update={"updated_at": datetime.utcnow()})
    tasks_db[task_id] = updated_task
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks_db[task_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
