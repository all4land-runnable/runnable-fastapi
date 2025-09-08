# app/routers/temp/temp_dto.py
from pydantic import BaseModel


class TempBase(BaseModel):
    message: str