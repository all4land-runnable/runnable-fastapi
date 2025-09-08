# app/routers/users/users_dto.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field  # EmailStr 제거

# 공통 입력 필드
class UserBase(BaseModel):
    email: str = Field(
        ...,
        description="사용자 이메일(로그인 ID로 사용 가능).",
        examples=["runnable@all4land.com"],
    )
    username: str = Field(
        ...,
        description="표시 이름(유니크).",
        examples=["올포랜드-1234"],
    )

# 생성용 입력 DTO
class UserCreate(UserBase):
    password: str = Field(
        ...,
        description="로그인 비밀번호(서버 저장 시 해시 권장).",
        examples=["runnable1234"],
    )
    age: int = Field(
        ...,
        description="나이(정수).",
        examples=[25],
    )
    runner_since: int = Field(
        ...,
        description="러닝 시작 연도(예: 2025).",
        examples=[2025],
    )
    pace_average: int = Field(
        ...,
        description="평균 페이스(초/킬로미터). 예: 390 == 6'30\"/km",
        examples=[390],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "email": "runnable@all4land.com",
                    "username": "올포랜드-1234",
                    "password": "runnable1234",
                    "age": 28,
                    "runner_since": 2022,
                    "pace_average": 390,
                }
            ]
        }
    )

# 부분 수정용 DTO
class UserUpdate(BaseModel):
    user_id: int = Field(
        ...,
        description="수정할 사용자 ID.",
        examples=[101],
    )
    email: Optional[str] = Field(
        None,
        description="수정할 이메일.",
        examples=["newmail@example.com"],
    )
    username: Optional[str] = Field(
        None,
        description="수정할 표시 이름(유니크).",
        examples=["올포랜드-patched"],
    )
    password: Optional[str] = Field(
        None,
        description="수정할 비밀번호(입력 시 해시 저장 권장).",
        examples=["newpass!234"],
    )
    age: Optional[int] = Field(
        None,
        description="수정할 나이.",
        examples=[29],
    )
    runner_since: Optional[int] = Field(
        None,
        description="수정할 러닝 시작 연도.",
        examples=[2021],
    )
    pace_average: Optional[int] = Field(
        None,
        description="수정할 평균 페이스(초/킬로미터).",
        examples=[380],
    )
    is_deleted: Optional[bool] = Field(
        None,
        description="소프트 삭제 플래그.",
        examples=[False],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "user_id": 101,
                    "email": "audwnssp@all4land.com",
                    "username": "김명준-1234",
                    "password": "gomj1234",
                    "age": 26,
                    "runner_since": 2024,
                    "pace_average": 280,
                    "is_deleted": True,
                }
            ]
        }
    )

# 삭제용 DTO
class UserDelete(BaseModel):
    user_id: int = Field(
        ...,
        description="삭제할 사용자 ID.",
        examples=[101],
    )

# 출력용 DTO
class UserOut(UserBase):
    user_id: int = Field(
        ...,
        description="사용자 ID(PK).",
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
                    "user_id": 101,
                    "email": "runnable@all4land.com",
                    "username": "올포랜드-1234",
                    "is_deleted": False,
                    "created_at": "2025-09-01T00:00:00Z",
                    "updated_at": "2025-09-08T19:05:12Z",
                }
            ]
        },
    )
