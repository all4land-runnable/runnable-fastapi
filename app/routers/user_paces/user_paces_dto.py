# app/routers/user_paces/user_paces_dto.py
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

# 공통 입력 필드
class UserPaceBase(BaseModel):
    user_strategy_id: int = Field(
        ...,
        description="사용자 전략 ID (user_strategies.user_strategy_id 참조).",
        examples=[501],
    )
    section_id: int = Field(
        ...,
        description="구간 ID (sections.section_id 참조).",
        examples=[301],
    )
    pace: int = Field(
        ...,
        description="구간 페이스(초/킬로미터). 예: 390 == 6'30\"/km",
        examples=[390],
    )
    strategy: str = Field(
        ...,
        description="적용한 전략의 이름/라벨(예: '컨서버티브', '포지티브 스플릿').",
        examples=["컨서버티브"],
    )
    foundation_latitude: float = Field(
        ...,
        description="전략 기준점 위도(WGS84).",
        examples=[37.5665],
    )
    foundation_longitude: float = Field(
        ...,
        description="전략 기준점 경도(WGS84).",
        examples=[126.9780],
    )

# 생성용 입력 DTO
class UserPaceCreate(UserPaceBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "user_strategy_id": 501,
                    "section_id": 301,
                    "pace": 390,
                    "strategy": "컨서버티브",
                    "foundation_latitude": 37.5665,
                    "foundation_longitude": 126.9780,
                }
            ]
        }
    )

# 부분 수정용 DTO
class UserPaceUpdate(BaseModel):
    user_pace_id: int = Field(
        ...,
        description="수정할 사용자 페이스 ID.",
        examples=[7001],
    )
    user_strategy_id: Optional[int] = Field(
        None,
        description="수정할 사용자 전략 ID.",
        examples=[502],
    )
    section_id: Optional[int] = Field(
        None,
        description="수정할 구간 ID.",
        examples=[302],
    )
    pace: Optional[int] = Field(
        None,
        description="수정할 구간 페이스(초/킬로미터).",
        examples=[380],
    )
    strategy: Optional[str] = Field(
        None,
        description="수정할 전략 라벨.",
        examples=["포지티브 스플릿"],
    )
    foundation_latitude: Optional[float] = Field(
        None,
        description="수정할 기준점 위도(WGS84).",
        examples=[37.57],
    )
    foundation_longitude: Optional[float] = Field(
        None,
        description="수정할 기준점 경도(WGS84).",
        examples=[126.98],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "user_pace_id": 7001,
                    "pace": 380,
                    "strategy": "포지티브 스플릿",
                }
            ]
        }
    )

# 출력용 DTO
class UserPaceOut(UserPaceBase):
    user_pace_id: int = Field(
        ...,
        description="사용자 페이스 ID(PK).",
        examples=[7001],
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "user_pace_id": 7001,
                    "user_strategy_id": 501,
                    "section_id": 301,
                    "pace": 390,
                    "strategy": "컨서버티브",
                    "foundation_latitude": 37.5665,
                    "foundation_longitude": 126.9780,
                }
            ]
        },
    )
