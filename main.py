from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional

from sentry_sdk import get_current_scope

from data_models.task import TaskCreate, TaskOut, TaskUpdate
from data_models.user import Role, UserCreate, UserOut, UserUpdate

app = FastAPI(title="Task Manager")

# in-memory "database"
fake_db: List[TaskOut] = []

@app.post("/tasks/", response_model=TaskOut)
def create_task(task: TaskCreate):
    new_task = TaskOut(**task.dict())
    fake_db.append(new_task)
    return new_task

@app.get("/tasks/", response_model=List[TaskOut])
def list_tasks():
    return fake_db

@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: UUID):
    for task in fake_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: UUID, update: TaskUpdate):
    for i, task in enumerate(fake_db):
        if task.id == task_id:
            updated_data = update.dict(exclude_unset=True)
            updated_task = task.copy(update=updated_data)
            fake_db[i] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: UUID):
    for i, task in enumerate(fake_db):
        if task.id == task_id:
            fake_db.pop(i)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")

# Fake in-memory DB for User Endpoints
# ---------------------------
users_db: Dict[UUID, Dict] = {}

# For User Endpoints ====

@app.post("/users", response_model=UserOut)
def create_user(payload: UserCreate):
    new_id = uuid4()
    record = payload.dict()
    record["id"] = new_id
    users_db[new_id] = record
    return UserOut(**record)

@app.get("/users", response_model=List[UserOut])
def list_users():
    return [UserOut(**u) for u in users_db.values()]

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: UUID):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(**user)

@app.patch("/users/{user_id}", response_model=UserOut)
def update_user(user_id: UUID, payload: UserUpdate):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = payload.dict(exclude_unset=True)
    user.update(update_data)
    users_db[user_id] = user
    return UserOut(**user)

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: UUID):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return None