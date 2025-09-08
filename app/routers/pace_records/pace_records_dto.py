# app/routers/pace_records/pace_records_dto.py
from pydantic import BaseModel, ConfigDict
from typing import Optional

class PaceRecordBase(BaseModel):
    record_id: int
    section_id: Optional[int] = None  # 모델이 nullable이므로 Optional
    pace: int

class PaceRecordCreate(PaceRecordBase):
    pass

class PaceRecordUpdate(BaseModel):
    pace_record_id: int
    record_id: Optional[int] = None
    section_id: Optional[int] = None
    pace: Optional[int] = None

class PaceRecordOut(PaceRecordBase):
    pace_record_id: int
    model_config = ConfigDict(from_attributes=True)
