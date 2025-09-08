# app/routers/user_paces/user_paces_dto.py
from typing import Optional
from pydantic import BaseModel, ConfigDict

# 공통 입력 필드
class UserPaceBase(BaseModel):
    user_strategy_id: int
    section_id: int

    pace: int
    strategy: str
    foundation_latitude: float
    foundation_longitude: float

# 생성용 입력 DTO
class UserPaceCreate(UserPaceBase):
    pass

# 부분 수정용 DTO
class UserPaceUpdate(BaseModel):
    user_pace_id: int
    user_strategy_id: Optional[int] = None
    section_id: Optional[int] = None
    pace: Optional[int] = None
    strategy: Optional[str] = None
    foundation_latitude: Optional[float] = None
    foundation_longitude: Optional[float] = None

# 출력용 DTO
class UserPaceOut(UserPaceBase):
    user_pace_id: int
    model_config = ConfigDict(from_attributes=True)
