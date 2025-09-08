# app/internal/exception/errorcode/user_strategies_error_code.py
from app.internal.exception.error_message import ErrorMessage

DUPLICATE_KEY = ErrorMessage(404, "중복된 사용자-루트 전략입니다.")
USER_STRATEGY_NOT_FOUND = ErrorMessage(404, "사용자-루트 전략을 찾을 수 없습니다.")
