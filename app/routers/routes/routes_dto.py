# app/routers/routes/routes_dto.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

# 공통 입력 필드
class RouteBase(BaseModel):
    title: str = None
    description: str
    distance: int
    high_height: float
    low_height: float

# 생성용 입력 DTO
class RouteCreate(RouteBase):
    pass

# 부분 수정용 DTO
class RouteUpdate(BaseModel):
    route_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    distance: Optional[int] = None
    high_height: Optional[float] = None
    low_height: Optional[float] = None
    is_deleted: Optional[bool] = None

# 삭제용 DTO
class RouteDelete(BaseModel):
    route_id: int

# 출력용 DTO
class RouteOut(RouteBase):
    route_id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
