from pydantic import BaseModel, Field
from typing import Optional, List


class UserCreate(BaseModel):
    username: str
    password: str = Field(min_length=6)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=30)
    password: Optional[str] = Field(None, min_length=6)


class TasksRelation(BaseModel):
    id: int
    title: str
    body: str


class UserCurrent(BaseModel):
    id: int
    username: str
    tasks: List[TasksRelation]


class UserCurrentUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=30)
    password: Optional[str] = Field(None, min_length=6)


class Users(BaseModel):
    id: int
    username: str
