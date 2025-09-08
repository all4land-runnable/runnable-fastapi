# app/routers/sections/sections_dto.py
from typing import Optional
from pydantic import BaseModel, ConfigDict


# 공통 입력 필드
class SectionBase(BaseModel):
    route_id: int

    start_latitude: float
    start_longitude: float
    start_height: float

    end_latitude: float
    end_longitude: float
    end_height: float

    slope: int  # TODO 타입 수정 시 DTO도 함께 반영


# 생성용 입력 DTO
class SectionCreate(SectionBase):
    pass


# 부분 수정용 DTO
class SectionUpdate(BaseModel):
    section_id: int
    route_id: Optional[int] = None

    start_latitude: Optional[float] = None
    start_longitude: Optional[float] = None
    start_height: Optional[float] = None

    end_latitude: Optional[float] = None
    end_longitude: Optional[float] = None
    end_height: Optional[float] = None

    slope: Optional[int] = None


# 출력용 DTO
class SectionOut(SectionBase):
    section_id: int

    model_config = ConfigDict(from_attributes=True)
