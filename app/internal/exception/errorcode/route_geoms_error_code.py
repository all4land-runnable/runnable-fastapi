# app/internal/exception/errorcode/route_geoms_error_code.py
from app.internal.exception.error_message import ErrorMessage

DUPLICATE_KEY = ErrorMessage(404, "중복된 경로 지오메트리입니다.")
ROUTE_GEOM_NOT_FOUND = ErrorMessage(404, "경로 지오메트리를 찾을 수 없습니다.")
