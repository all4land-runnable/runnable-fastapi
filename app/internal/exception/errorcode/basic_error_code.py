from app.internal.exception.error_message import ErrorMessage

ERROR_NOT_FOUND = ErrorMessage(404, "예기치 못한 오류")
ACCESS_DENIED = ErrorMessage(403, "접근 권한이 없음")
DATABASE_ERROR = ErrorMessage(404, "데이터베이스 접근 오류")
VALID_ERROR = ErrorMessage(404, "잘못된 객체 전달")