# app/routers/dataset/dataset_service.py
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from app.utils.radius_filter import radius_filter


class DatasetService:
    """
    요약:
        정적 JSON 데이터셋(음수대/횡단보도)을 로드하고,
        선택적으로 반경 필터링을 수행하는 서비스 레이어.

    설명:
        - 파일 경로는 항상 프로젝트 루트의 기본 경로만 사용한다.
        - 음수대는 lat/lng 좌표 기반의 일반 반경 필터를 사용한다.
        - 횡단보도는 WKT(Point/LineString* 포함) 파싱 후,
          각 좌표쌍을 (lon,lat)과 (lat,lon) 두 방식으로 해석해 반경 판정한다.
    """

    # [경로 상수] 프로젝트 루트 기준 기본 파일 경로 (항상 이 경로만 사용)
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    DEFAULT_DRINKING_PATH = PROJECT_ROOT / "routers" / "dataset" / "res" / "drinkingFountains.json"
    DEFAULT_CROSSWALKS_PATH = PROJECT_ROOT / "routers" / "dataset" / "res" / "crosswalks.json"

    # [지오 유틸 상수]
    EARTH_RADIUS_M = 6_371_000.0
    DEG2RAD = math.pi / 180.0

    # ---------- 내부 유틸 ----------
    def _read_default_json(self, path: Path) -> Dict[str, Any]:
        """항상 DEFAULT_* 경로에서만 JSON 로드. 파일 형식은 { "DATA": [...] } 가정."""
        return json.loads(path.read_text(encoding="utf-8"))

    def _haversine_m(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """두 좌표 간 하버사인 거리(m)."""
        lat1r, lon1r, lat2r, lon2r = (
            lat1 * self.DEG2RAD,
            lon1 * self.DEG2RAD,
            lat2 * self.DEG2RAD,
            lon2 * self.DEG2RAD,
        )
        dlat = lat2r - lat1r
        dlon = lon2r - lon1r
        a = (math.sin(dlat / 2) ** 2) + math.cos(lat1r) * math.cos(lat2r) * (math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return self.EARTH_RADIUS_M * c

    # ---- WKT 파서(견고 버전): POINT / LINESTRING / MULTILINESTRING, Z/M 옵션 지원 ----
    _num_re = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")

    def _scan_numbers(self, wkt: str) -> List[float]:
        """WKT 문자열에서 숫자만 추출."""
        return [float(x) for x in self._num_re.findall(wkt or "")]

    def _point_xy(self, wkt: str) -> Optional[Tuple[float, float]]:
        """POINT에서 (x,y) 한 쌍만 추출. 실패 시 None."""
        nums = self._scan_numbers(wkt)
        if len(nums) >= 2:
            return nums[0], nums[1]
        return None

    def _line_xy_list(self, wkt: str) -> List[Tuple[float, float]]:
        """
        LINESTRING / MULTILINESTRING 등에서 (x,y) 순서로 좌표쌍을 모두 추출.
        숫자들을 2개씩 끊어 (x,y) 리스트로 만든다.
        """
        nums = self._scan_numbers(wkt)
        out: List[Tuple[float, float]] = []
        for i in range(0, len(nums) - 1, 2):
            out.append((nums[i], nums[i + 1]))
        return out

    def _within_any_interpretation(
        self,
        cam_lat: float,
        cam_lon: float,
        x: float,
        y: float,
        radius_m: float,
    ) -> bool:
        """
        (x,y)를 (lon,lat)으로 해석하거나 (lat,lon)으로 해석했을 때
        둘 중 하나라도 반경 내면 True.
        """
        # 해석 1: (lon, lat)
        if self._haversine_m(cam_lat, cam_lon, y, x) <= radius_m:
            return True
        # 해석 2: (lat, lon)
        if self._haversine_m(cam_lat, cam_lon, x, y) <= radius_m:
            return True
        return False

    def _crosswalk_within_radius(self, obj: Dict[str, Any], cam_lat: float, cam_lon: float, radius_m: float) -> bool:
        """
        횡단보도 오브젝트가 반경 내인지 판별.
        - NODE: node_wkt(POINT)의 좌표를 (lon,lat)·(lat,lon) 모두 시도
        - LINK: lnkg_wkt(LINESTRING*/MULTI*)의 모든 버텍스에 대해 위 전략 적용
        """
        node_type = str(obj.get("node_type", "")).upper()

        # NODE → POINT
        if node_type == "NODE":
            xy = self._point_xy(obj.get("node_wkt", ""))
            if xy is not None:
                x, y = xy
                return self._within_any_interpretation(cam_lat, cam_lon, x, y, radius_m)
            # 좌표가 없으면 아래 라인 검사로 폴백

        # LINK/기타 → (멀티)라인의 모든 버텍스 검사
        for x, y in self._line_xy_list(obj.get("lnkg_wkt", "")):
            if self._within_any_interpretation(cam_lat, cam_lon, x, y, radius_m):
                return True
        return False

    # ---------- 공개 메서드 ----------
    def read_drinking_fountains(
        self,
        lat: Optional[float],
        lon: Optional[float],
        radius_m: float = 500.0,
    ) -> List[Dict[str, Any]]:
        """음수대 목록 조회(+선택적 반경 필터)"""
        payload = self._read_default_json(self.DEFAULT_DRINKING_PATH)
        data: List[Dict[str, Any]] = payload.get("DATA", [])
        if lat is not None and lon is not None:
            data = radius_filter(data, lat, lon, radius_m)  # dict의 "lat"/"lng" 사용
        return data

    def read_crosswalks(
        self,
        lat: Optional[float],
        lon: Optional[float],
        radius_m: float = 500.0,
    ) -> List[Dict[str, Any]]:
        """횡단보도 목록 조회(+선택적 반경 필터)"""
        payload = self._read_default_json(self.DEFAULT_CROSSWALKS_PATH)
        data: List[Dict[str, Any]] = payload.get("DATA", [])

        if lat is not None and lon is not None:
            cam_lat, cam_lon = float(lat), float(lon)
            data = [o for o in data if self._crosswalk_within_radius(o, cam_lat, cam_lon, radius_m)]

        return data
