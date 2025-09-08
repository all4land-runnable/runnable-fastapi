# app/utils/radius_filter.py
from __future__ import annotations

import math
from typing import Iterable, Any, Mapping, List, TypeVar

T = TypeVar("T")

EARTH_RADIUS_M = 6_371_000.0  # meters
DEG2RAD = math.pi / 180.0


def _get_lat_lon(o: Any) -> tuple[float, float]:
    """dict(키: lat/lng) 또는 속성(lat/lng) 모두 지원."""
    # dict 스타일 우선
    if isinstance(o, Mapping):
        lat_raw = o.get("lat")
        lon_raw = o.get("lng")
    else:
        lat_raw = getattr(o, "lat", None)
        lon_raw = getattr(o, "lng", None)

    if lat_raw is None or lon_raw is None:
        raise ValueError("lat/lng missing")

    return float(lat_raw), float(lon_raw)


def radius_filter(
    objects: Iterable[T],
    camera_lat: float,
    camera_lon: float,
    radius: float = 500.0,
) -> List[T]:
    """
    특정 반경(m) 안의 객체만 필터링하여 반환.

    objects: 각 원소가 lat/lng(도) 좌표를 가진 dict 또는 객체
    camera_lat / camera_lon: 기준 위경도(도)
    radius: 반경(m)
    """
    cam_lat_rad = camera_lat * DEG2RAD
    cam_lon_rad = camera_lon * DEG2RAD
    cos_cam_lat = math.cos(cam_lat_rad)

    out: List[T] = []
    for obj in objects or []:
        try:
            lat, lon = _get_lat_lon(obj)
        except (TypeError, ValueError):
            continue  # 좌표 없거나 변환 실패 → 스킵

        # 하버사인
        lat_rad = lat * DEG2RAD
        lon_rad = lon * DEG2RAD
        dlat = lat_rad - cam_lat_rad
        dlon = lon_rad - cam_lon_rad

        a = (math.sin(dlat / 2) ** 2) + cos_cam_lat * math.cos(lat_rad) * (math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = EARTH_RADIUS_M * c

        if distance <= radius:
            out.append(obj)

    return out
