# app/routers/points/points_dto.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

# 공통 입력 필드
class PointBase(BaseModel):
    section_id: int = Field(
        ...,
        description="소속 섹션 ID(FK: sections.section_id).",
        examples=[7],
    )
    index: int = Field(
        ...,
        description="섹션 내 순번(0 또는 1부터 등 정책에 맞춤).",
        examples=[0],
    )
    distance: float = Field(
        ...,
        description="섹션 시작으로부터 누적 거리(미터).",
        examples=[123.4],
    )
    latitude: float = Field(
        ...,
        description="위도(WGS84, 도).",
        examples=[37.5665],
    )
    longitude: float = Field(
        ...,
        description="경도(WGS84, 도).",
        examples=[126.9780],
    )
    height: float = Field(
        ...,
        description="고도(미터).",
        examples=[35.2],
    )

# 생성용 입력 DTO
class PointCreate(PointBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "section_id": 7,
                    "index": 0,
                    "distance": 0.0,
                    "latitude": 37.5665,
                    "longitude": 126.9780,
                    "height": 35.2,
                }
            ]
        }
    )

# 부분 수정용 DTO
class PointUpdate(BaseModel):
    point_id: int = Field(
        ...,
        description="수정할 포인트 ID(PK).",
        examples=[101],
    )
    section_id: Optional[int] = Field(
        None,
        description="수정할 섹션 ID(FK).",
        examples=[8],
    )
    index: Optional[int] = Field(
        None,
        description="수정할 섹션 내 순번.",
        examples=[1],
    )
    distance: Optional[float] = Field(
        None,
        description="수정할 누적 거리(미터).",
        examples=[150.0],
    )
    latitude: Optional[float] = Field(
        None,
        description="수정할 위도(WGS84).",
        examples=[37.5670],
    )
    longitude: Optional[float] = Field(
        None,
        description="수정할 경도(WGS84).",
        examples=[126.9790],
    )
    height: Optional[float] = Field(
        None,
        description="수정할 고도(미터).",
        examples=[36.0],
    )
    is_deleted: Optional[bool] = Field(
        None,
        description="소프트 삭제 플래그.",
        examples=[False],
    )

# 출력용 DTO
class PointOut(PointBase):
    point_id: int = Field(
        ...,
        description="포인트 ID(PK).",
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
        examples=["2025-09-10T00:00:00Z"],
    )
    updated_at: datetime = Field(
        ...,
        description="마지막 갱신 시각(타임존 포함).",
        examples=["2025-09-10T09:30:00Z"],
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "point_id": 101,
                    "section_id": 7,
                    "index": 0,
                    "distance": 0.0,
                    "latitude": 37.5665,
                    "longitude": 126.9780,
                    "height": 35.2,
                    "is_deleted": False,
                    "created_at": "2025-09-10T00:00:00Z",
                    "updated_at": "2025-09-10T09:30:00Z",
                }
            ]
        },
    )
