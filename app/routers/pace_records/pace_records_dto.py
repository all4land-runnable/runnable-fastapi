# app/routers/pace_records/pace_records_dto.py
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class PaceRecordBase(BaseModel):
    record_id: int = Field(
        ...,
        description="기록 ID(FK: records.record_id).",
        examples=[1001],
    )
    section_id: Optional[int] = Field(
        None,
        description="구간 ID(FK: sections.section_id). 없으면 전체(루트) 기준 페이스를 의미.",
        examples=[2001],
    )  # 모델이 nullable이므로 Optional
    pace: int = Field(
        ...,
        description="페이스(초/킬로미터). 예: 390 == 6'30\"/km",
        examples=[390],
    )

class PaceRecordCreate(PaceRecordBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"record_id": 1001, "section_id": 2001, "pace": 385},
                {"record_id": 1001, "pace": 392},  # section_id 생략(전체 기준)
            ]
        }
    )

class PaceRecordUpdate(BaseModel):
    pace_record_id: int = Field(
        ...,
        description="수정할 페이스 레코드 ID(PK).",
        examples=[5001],
    )
    record_id: Optional[int] = Field(
        None,
        description="수정할 기록 ID.",
        examples=[1002],
    )
    section_id: Optional[int] = Field(
        None,
        description="수정할 구간 ID. null로 변경하면 전체 기준으로 간주.",
        examples=[2002],
    )
    pace: Optional[int] = Field(
        None,
        description="수정할 페이스(초/킬로미터).",
        examples=[378],
    )

class PaceRecordOut(PaceRecordBase):
    pace_record_id: int = Field(
        ...,
        description="페이스 레코드 ID(PK).",
        examples=[5001],
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {"pace_record_id": 5001, "record_id": 1001, "section_id": 2001, "pace": 385},
                {"pace_record_id": 5002, "record_id": 1001, "section_id": None, "pace": 392},
            ]
        },
    )
