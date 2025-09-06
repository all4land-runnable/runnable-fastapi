from app.internal.exception.error_message import ErrorMessage

DUPLICATE_KEY = ErrorMessage(404, "중복된 이메일/아이디입니다.")
USER_NOT_FOUND = ErrorMessage(404, "사용자를 찾을 수 없습니다.")