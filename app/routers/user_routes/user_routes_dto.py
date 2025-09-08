# app/routers/user_routes/user_routes_dto.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

# 공통 입력 필드
class UserRouteBase(BaseModel):
    user_id: int = Field(
        ...,
        description="사용자 ID(users.user_id).",
        examples=[101],
    )
    category_id: int = Field(
        ...,
        description="카테고리 ID(categories.category_id).",
        examples=[11],
    )
    route_id: int = Field(
        ...,
        description="러닝 코스 ID(routes.route_id).",
        examples=[21],
    )

# 생성용 입력 DTO
class UserRouteCreate(UserRouteBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"user_id": 101, "category_id": 11, "route_id": 21}
            ]
        }
    )

# 부분 수정용 DTO
class UserRouteUpdate(BaseModel):
    user_route_id: int = Field(
        ...,
        description="수정할 사용자-코스 매핑 ID.",
        examples=[1001],
    )
    user_id: Optional[int] = Field(
        None,
        description="수정할 사용자 ID.",
        examples=[102],
    )
    category_id: Optional[int] = Field(
        None,
        description="수정할 카테고리 ID.",
        examples=[12],
    )
    route_id: Optional[int] = Field(
        None,
        description="수정할 코스 ID.",
        examples=[22],
    )
    is_deleted: Optional[bool] = Field(
        None,
        description="소프트 삭제 플래그.",
        examples=[False],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"user_route_id": 1001, "category_id": 12, "route_id": 22}
            ]
        }
    )

# 출력용 DTO
class UserRouteOut(UserRouteBase):
    user_route_id: int = Field(
        ...,
        description="사용자-코스 매핑 ID(PK).",
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
                    "user_route_id": 1001,
                    "user_id": 101,
                    "category_id": 11,
                    "route_id": 21,
                    "is_deleted": False,
                    "created_at": "2025-09-01T00:00:00Z",
                    "updated_at": "2025-09-08T19:05:12Z",
                }
            ]
        },
    )
