from app.internal.exception.error_message import ErrorMessage

JSON_PARSING_ERROR=ErrorMessage(-401, "LLM 답변 JSON 변환 실패")
INVALID_DATA_TYPE=ErrorMessage(-402, "잘못된 데이터 타입")