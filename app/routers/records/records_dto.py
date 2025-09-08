# app/routers/records/records_dto.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class RecordBase(BaseModel):
    user_route_id: int
    paces_average: int

class RecordCreate(RecordBase):
    pass

class RecordUpdate(BaseModel):
    record_id: int
    user_route_id: Optional[int] = None
    paces_average: Optional[int] = None

class RecordOut(RecordBase):
    record_id: int
    model_config = ConfigDict(from_attributes=True)
