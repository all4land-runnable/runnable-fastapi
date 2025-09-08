from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict  # EmailStr 제거

# 공통 입력 필드
class UserBase(BaseModel):
    email: str
    username: str

# 생성용 입력 DTO
class UserCreate(UserBase):
    password: str
    age: int
    runner_since: int
    pace_average: int

# 부분 수정용 DTO
class UserUpdate(BaseModel):
    user_id: int
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    age: Optional[int] = None
    runner_since: Optional[int] = None
    pace_average: Optional[int] = None
    is_deleted: Optional[bool] = None

# 삭제용 DTO
class UserDelete(BaseModel):
    user_id: int

# 출력용 DTO
class UserOut(UserBase):
    user_id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
