from app.internal.exception.error_message import ErrorMessage

DUPLICATE_KEY = ErrorMessage(404, "중복된 정보 입니다.")
ROUTE_NOT_FOUND = ErrorMessage(404, "경로를 찾을 수 없습니다.")