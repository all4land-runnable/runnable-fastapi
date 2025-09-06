from datetime import datetime

from pydantic import BaseModel


class Users(BaseModel):
    id: int
    email: str
    password: str
    username: str
    created_at: datetime
    updated_at: datetime