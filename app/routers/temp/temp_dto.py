# app/routers/temp/temp_dto.py
from pydantic import BaseModel, Field, ConfigDict

class TempBase(BaseModel):
    message: str = Field(
        ...,
        description="AI에게 전달할 입력값(프롬프트 원문).",
        examples=["오늘 러닝 코칭 플랜을 5km 기준으로 만들어줘"],
    )

    # 스웨거 예시
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"message": "내 평균 페이스 6'30\" 기준으로 10km 코스 추천해줘"}
            ]
        }
    )
