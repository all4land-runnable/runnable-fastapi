# app/routers/sections/sections_dto.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

# 공통 입력 필드
class SectionBase(BaseModel):
    route_id: int = Field(
        ...,
        description="구간이 속한 경로 ID(FK: routes.route_id).",
        examples=[42],
    )
    distance: float = Field(
        ...,
        description="구간 총 거리(미터, REAL).",
        examples=[250.0],
    )
    slope: float = Field(
        ...,
        description="구간 평균 경사(REAL). 단위 정의는 서비스 정책에 따름.",
        examples=[1.8],
    )

# 생성용 입력 DTO
class SectionCreate(SectionBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "route_id": 42,
                    "distance": 250.0,
                    "slope": 1.8,
                }
            ]
        }
    )

# 부분 수정용 DTO
class SectionUpdate(BaseModel):
    section_id: int = Field(
        ...,
        description="수정할 구간 ID(PK).",
        examples=[101],
    )
    route_id: Optional[int] = Field(
        None,
        description="수정할 경로 ID.",
        examples=[42],
    )
    distance: Optional[float] = Field(
        None,
        description="수정할 구간 총 거리(미터).",
        examples=[300.0],
    )
    slope: Optional[float] = Field(
        None,
        description="수정할 평균 경사.",
        examples=[2.5],
    )
    is_deleted: Optional[bool] = Field(
        None,
        description="소프트 삭제 플래그.",
        examples=[False],
    )

# 출력용 DTO
class SectionOut(SectionBase):
    section_id: int = Field(
        ...,
        description="구간 ID(PK).",
        examples=[101],
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
                    "section_id": 101,
                    "route_id": 42,
                    "distance": 250.0,
                    "slope": 1.8,
                    "is_deleted": False,
                    "created_at": "2025-09-01T00:00:00Z",
                    "updated_at": "2025-09-08T19:05:12Z",
                }
            ]
        },
    )
