# app/internal/exception/errorcode/user_routes_error_code.py
from app.internal.exception.error_message import ErrorMessage

DUPLICATE_KEY = ErrorMessage(404, "중복된 사용자-카테고리-루트 매핑입니다.")
USER_ROUTE_NOT_FOUND = ErrorMessage(404, "사용자-루트 매핑을 찾을 수 없습니다.")
