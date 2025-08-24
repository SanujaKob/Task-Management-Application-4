# routers/task.py
from typing import List, Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException, Response, status

from models.task import TaskCreate, TaskOut, TaskUpdate, Task

router = APIRouter()

# In-memory "DB" for tasks (module-level)
tasks_db: Dict[UUID, TaskOut] = {}


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    """
    Create a task. TaskCreate REQUIRES a UUID 'id' in the request body.
    """
    if payload.id in tasks_db:
        raise HTTPException(status_code=400, detail="Task with this ID already exists")

    # TaskOut adds timestamps; keep provided id + fields
    new_task = TaskOut(**payload.model_dump())
    tasks_db[new_task.id] = new_task
    return new_task


@router.get("", response_model=List[TaskOut])
def list_tasks():
    return list(tasks_db.values())


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: UUID):
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: UUID, payload: TaskUpdate):
    existing = tasks_db.get(task_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_data = payload.model_dump(exclude_unset=True)
    updated_task = existing.model_copy(update=updated_data)
    tasks_db[task_id] = updated_task
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks_db[task_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
