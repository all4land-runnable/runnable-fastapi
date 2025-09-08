# app/routers/routes/routes_dto.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

# 공통 입력 필드
class RouteBase(BaseModel):
    title: Optional[str] = Field(
        None,
        description="경로 제목(옵션). 비어 있으면 미지정 상태.",
        examples=["한강 러닝 코스 A"],
    )
    description: str = Field(
        ...,
        description="경로 설명(필수).",
        examples=["잠실-뚝섬 구간 왕복 10km 코스"],
    )
    distance: int = Field(
        ...,
        description="총 거리(미터). 예: 10000 == 10km",
        examples=[10000],
    )
    high_height: float = Field(
        ...,
        description="최고 고도(미터).",
        examples=[52.4],
    )
    low_height: float = Field(
        ...,
        description="최저 고도(미터).",
        examples=[18.7],
    )

# 생성용 입력 DTO
class RouteCreate(RouteBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "한강 러닝 코스 A",
                    "description": "잠실-뚝섬 구간 왕복 10km 코스",
                    "distance": 10000,
                    "high_height": 52.4,
                    "low_height": 18.7,
                }
            ]
        }
    )

# 부분 수정용 DTO
class RouteUpdate(BaseModel):
    route_id: int = Field(
        ...,
        description="수정할 경로 ID(PK).",
        examples=[101],
    )
    title: Optional[str] = Field(
        None,
        description="수정할 제목.",
        examples=["한강 러닝 코스 A(수정)"],
    )
    description: Optional[str] = Field(
        None,
        description="수정할 설명.",
        examples=["난이도/보행자 신호 구간 설명 추가"],
    )
    distance: Optional[int] = Field(
        None,
        description="수정할 총 거리(미터).",
        examples=[12000],
    )
    high_height: Optional[float] = Field(
        None,
        description="수정할 최고 고도(미터).",
        examples=[60.0],
    )
    low_height: Optional[float] = Field(
        None,
        description="수정할 최저 고도(미터).",
        examples=[15.0],
    )
    is_deleted: Optional[bool] = Field(
        None,
        description="소프트 삭제 플래그.",
        examples=[False],
    )

# 삭제용 DTO
class RouteDelete(BaseModel):
    route_id: int = Field(
        ...,
        description="삭제할 경로 ID(PK).",
        examples=[101],
    )

# 출력용 DTO
class RouteOut(RouteBase):
    route_id: int = Field(
        ...,
        description="경로 ID(PK).",
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
                    "route_id": 101,
                    "title": "한강 러닝 코스 A",
                    "description": "잠실-뚝섬 구간 왕복 10km 코스",
                    "distance": 10000,
                    "high_height": 52.4,
                    "low_height": 18.7,
                    "is_deleted": False,
                    "created_at": "2025-09-01T00:00:00Z",
                    "updated_at": "2025-09-08T19:05:12Z",
                }
            ]
        },
    )
