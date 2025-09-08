# app/internal/exception/errorcode/rank_error_code.py
from app.internal.exception.error_message import ErrorMessage

RANK_NOT_FOUND = ErrorMessage(404, "랭크를 찾을 수 없습니다.")
DUPLICATE_KEY = ErrorMessage(404, "중복된 랭크가 존재합니다.")
