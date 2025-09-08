# app/routers/categories/categories_dto.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

# 공통 입력 필드
class CategoryBase(BaseModel):
    user_id: int
    name: str

# 생성용 입력 DTO
class CategoryCreate(CategoryBase):
    pass

# 부분 수정용 DTO
class CategoryUpdate(BaseModel):
    category_id: int
    user_id: Optional[int] = None
    name: Optional[str] = None
    is_deleted: Optional[bool] = None

# 출력용 DTO
class CategoryOut(CategoryBase):
    category_id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
