from pydantic import BaseModel
from datetime import date, datetime

# ======================
# USER SCHEMA
# ======================

class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


# ======================
# TASK SCHEMA
# ======================

class TaskBase(BaseModel):
    title: str
    description: str
    status: str
    deadline: date
    assignee_id: int


class TaskCreate(TaskBase):
    pass


class TaskOut(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
