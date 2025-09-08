# app/routers/available_times/available_times_dto.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

# 공통 입력 필드
class AvailableTimeBase(BaseModel):
    route_id: int
    since: datetime
    start_time: datetime
    end_time: datetime

# 생성용 입력 DTO
class AvailableTimeCreate(AvailableTimeBase):
    pass

# 부분 수정용 DTO
class AvailableTimeUpdate(BaseModel):
    available_time_id: int
    route_id: Optional[int] = None
    since: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_deleted: Optional[bool] = None

# 출력용 DTO
class AvailableTimeOut(AvailableTimeBase):
    available_time_id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
