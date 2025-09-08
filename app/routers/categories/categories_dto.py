# app/routers/categories/categories_dto.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

# 공통 입력 필드
class CategoryBase(BaseModel):
    user_id: int = Field(
        ...,
        description="카테고리 소유 사용자 ID(FK: users.user_id).",
        examples=[101],
    )
    name: str = Field(
        ...,
        description="카테고리 이름(예: 출퇴근 러닝, 주말 롱런 등).",
        examples=["출퇴근 러닝"],
    )

# 생성용 입력 DTO
class CategoryCreate(CategoryBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"user_id": 101, "name": "주말 롱런"},
                {"user_id": 101, "name": "인터벌 트레이닝"},
            ]
        }
    )

# 부분 수정용 DTO
class CategoryUpdate(BaseModel):
    category_id: int = Field(
        ...,
        description="수정할 카테고리 ID(PK).",
        examples=[1001],
    )
    user_id: Optional[int] = Field(
        None,
        description="소유 사용자 ID 변경 시 지정.",
        examples=[102],
    )
    name: Optional[str] = Field(
        None,
        description="카테고리명 변경 시 지정.",
        examples=["평일 가벼운 조깅"],
    )
    is_deleted: Optional[bool] = Field(
        None,
        description="소프트 삭제 플래그.",
        examples=[False],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"category_id": 1001, "name": "평일 가벼운 조깅"},
                {"category_id": 1001, "is_deleted": True},
            ]
        }
    )

# 출력용 DTO
class CategoryOut(CategoryBase):
    category_id: int = Field(
        ...,
        description="카테고리 ID(PK).",
        examples=[1001],
    )
    is_deleted: bool = Field(
        ...,
        description="소프트 삭제 여부.",
        examples=[False],
    )
    created_at: datetime = Field(
        ...,
        description="생성 시각(타임존 포함).",
        examples=["2025-09-01T00:00:00Z"],
    )
    updated_at: datetime = Field(
        ...,
        description="마지막 갱신 시각(타임존 포함).",
        examples=["2025-09-08T19:05:12Z"],
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "category_id": 1001,
                    "user_id": 101,
                    "name": "출퇴근 러닝",
                    "is_deleted": False,
                    "created_at": "2025-09-01T00:00:00Z",
                    "updated_at": "2025-09-08T19:05:12Z",
                }
            ]
        },
    )
