# app/internal/exception/errorcode/user_paces_error_code.py
from app.internal.exception.error_message import ErrorMessage

DUPLICATE_KEY = ErrorMessage(404, "중복된 사용자 페이스 입니다.")
USER_PACE_NOT_FOUND = ErrorMessage(404, "사용자 페이스를 찾을 수 없습니다.")
