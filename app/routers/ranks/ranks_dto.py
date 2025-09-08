# app/routers/ranks/ranks_dto.py
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class RankBase(BaseModel):
    record_id: int = Field(
        ...,
        description="순위를 매길 기록 ID(FK: records.record_id).",
        examples=[1001],
    )
    rank: int = Field(
        ...,
        description="해당 기록의 순위(1이 최고).",
        examples=[1],
    )

class RankCreate(RankBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "record_id": 1001,
                    "rank": 1,
                }
            ]
        }
    )

class RankUpdate(BaseModel):
    rank_id: int = Field(
        ...,
        description="수정할 랭크 ID(PK).",
        examples=[501],
    )
    record_id: Optional[int] = Field(
        None,
        description="수정할 기록 ID.",
        examples=[1002],
    )
    rank: Optional[int] = Field(
        None,
        description="수정할 순위 값.",
        examples=[2],
    )

class RankOut(RankBase):
    rank_id: int = Field(
        ...,
        description="랭크 ID(PK).",
        examples=[501],
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "rank_id": 501,
                    "record_id": 1001,
                    "rank": 1,
                }
            ]
        },
    )
