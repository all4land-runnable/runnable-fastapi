from langchain_core.exceptions import ErrorCode

DUPLICATE_KEY = ErrorCode(409, "중복 키 오류(포인트)")
POINT_NOT_FOUND = ErrorCode(404, "포인트를 찾을 수 없습니다.")
INVALID_REQUEST = ErrorCode(400, "유효하지 않은 포인트 요청입니다.")