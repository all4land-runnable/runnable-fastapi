# app/routers/available_times/available_times_dto.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

# 공통 입력 필드
class AvailableTimeBase(BaseModel):
    route_id: int = Field(
        ...,
        description="대상 경로 ID(FK: routes.route_id).",
        examples=[1],
    )
    since: datetime = Field(
        ...,
        description="이 시간 정보가 유효해진 기준 시각(예: 정책 적용 시작 시각, ISO-8601).",
        examples=["2025-09-01T00:00:00Z"],
    )
    start_time: datetime = Field(
        ...,
        description="러닝/활동 시작 가능 시각(ISO-8601, 타임존 포함 권장).",
        examples=["2025-09-08T09:00:00Z"],
    )
    end_time: datetime = Field(
        ...,
        description="러닝/활동 종료 가능 시각(ISO-8601, 타임존 포함 권장).",
        examples=["2025-09-08T11:30:00Z"],
    )

# 생성용 입력 DTO
class AvailableTimeCreate(AvailableTimeBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "route_id": 1,
                    "since": "2025-09-01T00:00:00Z",
                    "start_time": "2025-09-08T09:00:00Z",
                    "end_time": "2025-09-08T11:30:00Z",
                }
            ]
        }
    )

# 부분 수정용 DTO
class AvailableTimeUpdate(BaseModel):
    available_time_id: int = Field(
        ...,
        description="수정할 가용 시간 ID(PK).",
        examples=[1001],
    )
    route_id: Optional[int] = Field(
        None,
        description="대상 경로 ID 변경 시 지정.",
        examples=[2],
    )
    since: Optional[datetime] = Field(
        None,
        description="유효 시작 기준 시각 변경(ISO-8601).",
        examples=["2025-09-02T00:00:00Z"],
    )
    start_time: Optional[datetime] = Field(
        None,
        description="시작 가능 시각 변경(ISO-8601).",
        examples=["2025-09-08T08:30:00Z"],
    )
    end_time: Optional[datetime] = Field(
        None,
        description="종료 가능 시각 변경(ISO-8601).",
        examples=["2025-09-08T12:00:00Z"],
    )
    is_deleted: Optional[bool] = Field(
        None,
        description="소프트 삭제 플래그.",
        examples=[False],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"available_time_id": 1001, "start_time": "2025-09-08T08:30:00Z"},
                {"available_time_id": 1001, "is_deleted": True},
            ]
        }
    )

# 출력용 DTO
class AvailableTimeOut(AvailableTimeBase):
    available_time_id: int = Field(
        ...,
        description="가용 시간 ID(PK).",
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
                    "available_time_id": 1001,
                    "route_id": 1,
                    "since": "2025-09-01T00:00:00Z",
                    "start_time": "2025-09-08T09:00:00Z",
                    "end_time": "2025-09-08T11:30:00Z",
                    "is_deleted": False,
                    "created_at": "2025-09-01T00:00:00Z",
                    "updated_at": "2025-09-08T19:05:12Z",
                }
            ]
        },
    )
