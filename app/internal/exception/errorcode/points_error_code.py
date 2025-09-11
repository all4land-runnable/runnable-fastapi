from app.internal.exception.error_message import ErrorMessage

DUPLICATE_KEY = ErrorMessage(409, "중복 키 오류(포인트)")
POINT_NOT_FOUND = ErrorMessage(404, "포인트를 찾을 수 없습니다.")
INVALID_REQUEST = ErrorMessage(400, "유효하지 않은 포인트 요청입니다.")