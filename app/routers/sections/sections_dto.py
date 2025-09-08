# app/routers/sections/sections_dto.py
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


# 공통 입력 필드
class SectionBase(BaseModel):
    route_id: int = Field(
        ...,
        description="구간이 속한 경로 ID(PK: routes.route_id).",
        examples=[42],
    )

    start_latitude: float = Field(
        ...,
        description="구간 시작 지점 위도(WGS84, 도 단위).",
        examples=[37.5665],
    )
    start_longitude: float = Field(
        ...,
        description="구간 시작 지점 경도(WGS84, 도 단위).",
        examples=[126.9780],
    )
    start_height: float = Field(
        ...,
        description="구간 시작 지점 고도(미터).",
        examples=[35.2],
    )

    end_latitude: float = Field(
        ...,
        description="구간 종료 지점 위도(WGS84, 도 단위).",
        examples=[37.5701],
    )
    end_longitude: float = Field(
        ...,
        description="구간 종료 지점 경도(WGS84, 도 단위).",
        examples=[126.9903],
    )
    end_height: float = Field(
        ...,
        description="구간 종료 지점 고도(미터).",
        examples=[41.0],
    )

    slope: int = Field(
        ...,
        description="구간 평균 경사(정수). 단위/타입은 추후 확정 예정(예: ‰ 또는 %).  # TODO 타입 수정 시 DTO도 함께 반영",
        examples=[35],
    )


# 생성용 입력 DTO
class SectionCreate(SectionBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "route_id": 42,
                    "start_latitude": 37.5665,
                    "start_longitude": 126.9780,
                    "start_height": 35.2,
                    "end_latitude": 37.5701,
                    "end_longitude": 126.9903,
                    "end_height": 41.0,
                    "slope": 35,
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

    start_latitude: Optional[float] = Field(
        None,
        description="수정할 시작 지점 위도(WGS84).",
        examples=[37.5670],
    )
    start_longitude: Optional[float] = Field(
        None,
        description="수정할 시작 지점 경도(WGS84).",
        examples=[126.9790],
    )
    start_height: Optional[float] = Field(
        None,
        description="수정할 시작 지점 고도(미터).",
        examples=[36.0],
    )

    end_latitude: Optional[float] = Field(
        None,
        description="수정할 종료 지점 위도(WGS84).",
        examples=[37.5710],
    )
    end_longitude: Optional[float] = Field(
        None,
        description="수정할 종료 지점 경도(WGS84).",
        examples=[126.9910],
    )
    end_height: Optional[float] = Field(
        None,
        description="수정할 종료 지점 고도(미터).",
        examples=[42.3],
    )

    slope: Optional[int] = Field(
        None,
        description="수정할 평균 경사(정수). 단위/타입은 추후 확정 예정.",
        examples=[30],
    )


# 출력용 DTO
class SectionOut(SectionBase):
    section_id: int = Field(
        ...,
        description="구간 ID(PK).",
        examples=[101],
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "section_id": 101,
                    "route_id": 42,
                    "start_latitude": 37.5665,
                    "start_longitude": 126.9780,
                    "start_height": 35.2,
                    "end_latitude": 37.5701,
                    "end_longitude": 126.9903,
                    "end_height": 41.0,
                    "slope": 35,
                }
            ]
        },
    )
