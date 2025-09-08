# app/internal/exception/errorcode/pace_records_error_code.py
from app.internal.exception.error_message import ErrorMessage

PACE_RECORD_NOT_FOUND = ErrorMessage(404, "페이스 기록을 찾을 수 없습니다.")
DUPLICATE_KEY = ErrorMessage(404, "중복된 페이스 기록이 존재합니다.")
