# app/internal/exception/errorcode/available_times_error_code.py
from app.internal.exception.error_message import ErrorMessage

AVAILABLE_TIME_NOT_FOUND = ErrorMessage(404, "이용 가능 시간을 찾을 수 없습니다.")
DUPLICATE_KEY = ErrorMessage(404, "중복된 이용 가능 시간이 존재합니다.")  # (모델에 유니크 제약이 없으면 실제로는 거의 발생 X)
