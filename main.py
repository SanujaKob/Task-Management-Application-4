# main.py
from fastapi import FastAPI

from routers.task import router as tasks_router
from routers.user import router as employees_router  # file 'user.py' but employee endpoints

app = FastAPI(title="Task Manager")

# Attach routers
app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
app.include_router(employees_router, prefix="/employees", tags=["Employees"])
