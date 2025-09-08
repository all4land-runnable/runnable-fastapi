# app/routers/user_strategies/user_strategies_dto.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

# 공통 입력 필드
class UserStrategyBase(BaseModel):
    user_route_id: int
    luggage_weight: int
    pace_average: int

# 생성용 입력 DTO
class UserStrategyCreate(UserStrategyBase):
    pass

# 부분 수정용 DTO
class UserStrategyUpdate(BaseModel):
    user_strategy_id: int
    user_route_id: Optional[int] = None
    luggage_weight: Optional[int] = None
    pace_average: Optional[int] = None
    is_deleted: Optional[bool] = None

# 출력용 DTO
class UserStrategyOut(UserStrategyBase):
    user_strategy_id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
