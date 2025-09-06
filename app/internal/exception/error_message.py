from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorMessage:
    """
    요약:
        예측 가능한 에러를 상수로 명시해둔 ErrorCode 클래스

    설명:
        각 반환 코드는 음수로 표시된다.
        첫번째 값은 에러들의 항목을 의미한다.

    Attributes:
        code(int): 에러코드
        message(str): 에러 메세지
    """
    code: int
    message: str