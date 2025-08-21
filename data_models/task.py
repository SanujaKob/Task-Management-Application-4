from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from enum import Enum
from uuid import UUID

# ---- Enums ----
class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class Status(str, Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"
    approved = "approved"
    rejected = "rejected"
    re_submit = "re_submit"

# ---- Common shared fields ----
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Priority = Priority.low
    status: Status = Status.not_started
    progress: int = Field(0, ge=0, le=100)
    due_date: Optional[date] = None
    assignee_id: Optional[int] = None  # can switch to UUID later

# ---- Mix-in that forces a mandatory UUID ----
class TaskIdMixin(BaseModel):
    id: UUID  # REQUIRED (no default_factory)

# ---- For POST /tasks ----
# Client MUST supply a UUID for the task they create.
class TaskCreate(TaskIdMixin, TaskBase):
    pass

# ---- For PATCH/PUT /tasks/{id} ----
# Only changing fields; id typically comes from the URL/path.
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[Status] = None
    progress: Optional[int] = Field(None, ge=0, le=100)
    due_date: Optional[date] = None
    assignee_id: Optional[int] = None

# ---- What you send back to Manager/UI ----
class TaskOut(TaskIdMixin, TaskBase):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
