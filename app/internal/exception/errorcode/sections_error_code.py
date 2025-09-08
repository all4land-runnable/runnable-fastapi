# app/internal/exception/errorcode/sections_error_code.py
from app.internal.exception.error_message import ErrorMessage

DUPLICATE_KEY = ErrorMessage(404, "중복된 섹션 데이터 입니다.")
SECTION_NOT_FOUND = ErrorMessage(404, "섹션을 찾을 수 없습니다.")
