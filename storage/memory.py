from typing import Dict, List, Optional
from uuid import UUID
from models.user import User, EmployeeCreate, Role
from models.task import Task, TaskCreate, TaskUpdate
from routers.assignments import assignments_router

# In-memory stores (pretend DB tables)
USERS: Dict[UUID, User] = {}
TASKS: Dict[UUID, Task] = {}

# ---- USERS ----
def create_user(data: EmployeeCreate) -> User:
    user = User(**data.model_dump())
    USERS[user.id] = user
    return user

def get_user(user_id: UUID) -> Optional[User]:
    return USERS.get(user_id)

def list_users(role: Optional[Role] = None) -> List[User]:
    values = list(USERS.values())
    return [u for u in values if role is None or u.role == role]

# ---- TASKS ----
def create_task(data: TaskCreate) -> Task:
    # Referential integrity: if assignee specified, must exist AND be an employee
    if data.assignee_id is not None:
        user = get_user(data.assignee_id)
        if user is None:
            raise ValueError("Assignee does not exist.")
        if user.role not in (Role.employee, Role.manager):  # allow manager too if needed
            raise ValueError("Assignee must be an employee or manager.")
    task = Task(**data.model_dump())
    TASKS[task.id] = task
    return task

def update_task(task_id: UUID, data: TaskUpdate) -> Task:
    task = TASKS.get(task_id)
    if not task:
        raise KeyError("Task not found.")
    # If reassigning, validate target
    if data.assignee_id is not None:
        user = get_user(data.assignee_id)
        if user is None:
            raise ValueError("Assignee does not exist.")
        if user.role not in (Role.employee, Role.manager):
            raise ValueError("Assignee must be an employee or manager.")
    merged = task.model_dump()
    for k, v in data.model_dump(exclude_unset=True).items():
        merged[k] = v
    new_task = Task(**merged)
    TASKS[task_id] = new_task
    return new_task

def get_task(task_id: UUID) -> Optional[Task]:
    return TASKS.get(task_id)

def delete_task(task_id: UUID) -> bool:
    return TASKS.pop(task_id, None) is not None

def list_tasks() -> List[Task]:
    return list(TASKS.values())

def list_tasks_by_assignee(user_id: UUID) -> List[Task]:
    return [t for t in TASKS.values() if t.assignee_id == user_id]
