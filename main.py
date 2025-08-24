# main.py
from fastapi import FastAPI

# --- DB base & models (ensure models are imported before create_all) ---
from database import Base, engine
import models.user  # noqa: F401
import models.task  # noqa: F401

# --- Routers ---
from routers.task import router as tasks_router
from routers.user import router as employees_router
from routers.assignments import router as assignments_router  # NEW

app = FastAPI(title="ABACUS Task Management Application")

# Create tables (for simple setups; switch to Alembic for migrations later)
Base.metadata.create_all(bind=engine)

# Mount routers
app.include_router(employees_router, prefix="/employees", tags=["Employees"])
app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
app.include_router(assignments_router, prefix="/assignments", tags=["Assignments"])  # NEW

# Optional: a simple health/root endpoint
@app.get("/", tags=["Health"])
def read_root():
    return {"status": "ok", "service": "ABACUS Task Management Application"}
