from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator
from app.tasks import choices


class TaskCreate(BaseModel):
    title: str
    body: str
    execution_datetime: datetime


class TaskUpdate(BaseModel):
    title: str
    body: str
    execution_datetime: datetime
    status: choices.TaskStatus


class UserRelation(BaseModel):
    id: int
    username: str


class Tasks(BaseModel):
    title: str
    body: str
    execution_datetime: Optional[datetime]
    status: choices.TaskStatus
    # user: UserRelation

    @validator("body", pre=True, always=True)
    def truncate_body(cls, value):
        if len(value) > 15:
            return value[:15] + "..."
        return value


class Task(BaseModel):
    title: str
    body: str
    execution_datetime: Optional[datetime]
    status: choices.TaskStatus
