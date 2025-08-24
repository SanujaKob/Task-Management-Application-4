from fastapi import FastAPI
from database import Base, engine
import models.user
import models.task

from routers.task import router as tasks_router
from routers.user import router as employees_router

app = FastAPI(title="ABACUS Task Management Application")

# create tables
Base.metadata.create_all(bind=engine)

# routers
app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
app.include_router(employees_router, prefix="/employees", tags=["Employees"])
