# app/internal/exception/errorcode/categories_error_code.py
from app.internal.exception.error_message import ErrorMessage

DUPLICATE_KEY = ErrorMessage(404, "중복된 카테고리명 입니다.")
CATEGORY_NOT_FOUND = ErrorMessage(404, "카테고리를 찾을 수 없습니다.")
