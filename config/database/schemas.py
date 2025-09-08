# config/database/schemas.py
from pydantic import BaseModel


class TodoItemCreate(BaseModel):
    title: str
    description: str | None = None

class TodoItem(BaseModel):
    id: int
    title: str
    description: str | None = None
    done: bool

    class Config:
        orm_mode = True