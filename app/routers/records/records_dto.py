# app/routers/records/records_dto.py
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class RecordBase(BaseModel):
    user_route_id: int = Field(
        ...,
        description="기록이 속한 사용자 경로 매핑 ID(FK: user_routes.user_route_id).",
        examples=[501],
    )
    paces_average: int = Field(
        ...,
        description="전체 평균 페이스(초/킬로미터). 예: 390 ⇒ 6'30\"/km",
        examples=[390],
    )

class RecordCreate(RecordBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "user_route_id": 501,
                    "paces_average": 385,
                }
            ]
        }
    )

class RecordUpdate(BaseModel):
    record_id: int = Field(
        ...,
        description="수정할 기록 ID(PK).",
        examples=[1001],
    )
    user_route_id: Optional[int] = Field(
        None,
        description="수정할 사용자 경로 매핑 ID.",
        examples=[502],
    )
    paces_average: Optional[int] = Field(
        None,
        description="수정할 평균 페이스(초/킬로미터).",
        examples=[380],
    )

class RecordOut(RecordBase):
    record_id: int = Field(
        ...,
        description="기록 ID(PK).",
        examples=[1001],
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "record_id": 1001,
                    "user_route_id": 501,
                    "paces_average": 385,
                }
            ]
        },
    )
