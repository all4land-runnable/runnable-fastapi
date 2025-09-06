from datetime import datetime

from pydantic import BaseModel


class UsersDTO(BaseModel):
    id: int
    email: str
    password: str
    username: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()