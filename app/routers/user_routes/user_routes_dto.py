# app/routers/user_routes/user_routes_dto.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

# 공통 입력 필드
class UserRouteBase(BaseModel):
    user_id: int
    category_id: int
    route_id: int

# 생성용 입력 DTO
class UserRouteCreate(UserRouteBase):
    pass

# 부분 수정용 DTO
class UserRouteUpdate(BaseModel):
    user_route_id: int
    user_id: Optional[int] = None
    category_id: Optional[int] = None
    route_id: Optional[int] = None
    is_deleted: Optional[bool] = None

# 출력용 DTO
class UserRouteOut(UserRouteBase):
    user_route_id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
