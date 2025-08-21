from uuid import UUID, uuid4
from typing import Dict, List

from fastapi import FastAPI, HTTPException, Response, status

# ---- Import your updated models ----
from data_models.task import TaskCreate, TaskOut, TaskUpdate
from data_models.user import Role, EmployeeCreate, EmployeeOut, EmployeeUpdate

app = FastAPI(title="Task Manager")

# =====================================================
# In-memory "databases"
# =====================================================
tasks_db: Dict[UUID, TaskOut] = {}
employees_db: Dict[UUID, dict] = {}

# =====================================================
# TASKS
# =====================================================

@app.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(payload: TaskCreate):
    """
    Create a task. NOTE: TaskCreate requires a UUID id (mandatory).
    """
    # Ensure no duplicates
    if payload.id in tasks_db:
        raise HTTPException(status_code=400, detail="Task with this ID already exists")

    # TaskOut will add timestamps; keep the provided id and other fields
    new_task = TaskOut(**payload.model_dump())
    tasks_db[new_task.id] = new_task
    return new_task


@app.get("/tasks", response_model=List[TaskOut], tags=["Tasks"])
def list_tasks():
    return list(tasks_db.values())


@app.get("/tasks/{task_id}", response_model=TaskOut, tags=["Tasks"])
def get_task(task_id: UUID):
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=TaskOut, tags=["Tasks"])
def update_task(task_id: UUID, payload: TaskUpdate):
    """
    Full/partial update via TaskUpdate (all fields optional).
    """
    existing = tasks_db.get(task_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_data = payload.model_dump(exclude_unset=True)
    updated_task = existing.model_copy(update=updated_data)
    tasks_db[task_id] = updated_task
    return updated_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
def delete_task(task_id: UUID):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks_db[task_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# =====================================================
# EMPLOYEES
# =====================================================

@app.post("/employees", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED, tags=["Employees"])
def create_employee(payload: EmployeeCreate):
    """
    Create an employee. We generate the UUID here.
    """
    new_id = uuid4()
    record = payload.model_dump()
    record["id"] = new_id
    employees_db[new_id] = record
    return EmployeeOut(**record)


@app.get("/employees", response_model=List[EmployeeOut], tags=["Employees"])
def list_employees():
    return [EmployeeOut(**e) for e in employees_db.values()]


@app.get("/employees/{employee_id}", response_model=EmployeeOut, tags=["Employees"])
def get_employee(employee_id: UUID):
    emp = employees_db.get(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return EmployeeOut(**emp)


@app.patch("/employees/{employee_id}", response_model=EmployeeOut, tags=["Employees"])
def update_employee(employee_id: UUID, payload: EmployeeUpdate):
    emp = employees_db.get(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    update_data = payload.model_dump(exclude_unset=True)
    emp.update(update_data)
    employees_db[employee_id] = emp
    return EmployeeOut(**emp)


@app.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Employees"])
def delete_employee(employee_id: UUID):
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    del employees_db[employee_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
