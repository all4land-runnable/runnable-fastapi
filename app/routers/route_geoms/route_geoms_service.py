# app/routers/route_geoms/route_geoms_service.py
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, select

from app.internal.exception.controlled_exception import ControlledException
from app.internal.exception.errorcode import route_geoms_error_code
from app.routers.route_geoms.route_geoms import RouteGeoms
from app.routers.route_geoms.route_geoms_dto import RouteGeomCreate, RouteGeomUpdate, RouteGeomOut  # ← Out 사용
from app.routers.route_geoms.route_geoms_repository import RouteGeomsRepository

class RouteGeomsService:
    def __init__(self, database: Session, route_geoms_repository: RouteGeomsRepository) -> None:
        # Service는 트랜잭션 경계(Commit/Rollback) + 의미있는 예외 매핑 담당.
        self.database = database
        self.route_geoms_repository = route_geoms_repository

    # 내부 유틸: 문자열 입력을 PostGIS Geometry 식으로 변환
    def _coerce_geom_input(self, geom_str: str):
        """
        - GeoJSON: ST_GeomFromGeoJSON → ST_SetSRID(…, 4326)
        - WKT:     ST_GeomFromText(…, 4326)
        """
        s = (geom_str or "").strip()
        if s.startswith("{") or s.startswith("["):  # 매우 단순한 GeoJSON 감지
            return func.ST_SetSRID(func.ST_GeomFromGeoJSON(s), 4326)
        # 기본은 WKT로 처리 (예: 'LINESTRING(127.0 37.5, 127.01 37.51)')
        return func.ST_GeomFromText(s, 4326)

    # 내부 유틸: 엔티티 → DTO(geom은 GeoJSON 문자열로 직렬화)
    def _to_out(self, rg: RouteGeoms) -> RouteGeomOut:
        geojson = self.database.scalar(
            select(func.ST_AsGeoJSON(RouteGeoms.geom)).where(RouteGeoms.route_geom_id == rg.route_geom_id)
        )
        return RouteGeomOut(route_geom_id=rg.route_geom_id, route_id=rg.route_id, geom=geojson)

    # 생성
    def create_route_geom(self, dto: RouteGeomCreate) -> RouteGeomOut:
        rg = RouteGeoms(route_id=dto.route_id, geom=self._coerce_geom_input(dto.geom))
        try:
            self.route_geoms_repository.save(rg)   # flush까지 하고 PK 확보
            self.database.commit()                 # [핵심] 트랜잭션 확정은 Service에서만
        except IntegrityError as e:
            self.database.rollback()
            # 유니크/FK 위반 등 → 비즈니스 에러코드로 변환
            raise ControlledException(route_geoms_error_code.DUPLICATE_KEY) from e

        self.database.refresh(rg)                  # server_default/trigger 동기화
        return self._to_out(rg)

    # 조회 (없으면 예외)
    def find_by_id(self, route_geom_id: int) -> RouteGeomOut:
        rg = self.route_geoms_repository.find_by_id(route_geom_id)
        if not rg:
            raise ControlledException(route_geoms_error_code.ROUTE_GEOM_NOT_FOUND)
        return self._to_out(rg)

    def find_all(self) -> List[RouteGeomOut]:
        lst = self.route_geoms_repository.find_all()
        if not lst:
            # 빈 리스트 허용하려면 이 예외 제거
            raise ControlledException(route_geoms_error_code.ROUTE_GEOM_NOT_FOUND)
        return [self._to_out(rg) for rg in lst]

    def find_by_route_id(self, route_id: int) -> List[RouteGeomOut]:
        lst = self.route_geoms_repository.find_by_route_id(route_id)
        if not lst:
            raise ControlledException(route_geoms_error_code.ROUTE_GEOM_NOT_FOUND)
        return [self._to_out(rg) for rg in lst]

    # 갱신
    def update_route_geom(self, dto: RouteGeomUpdate) -> RouteGeomOut:
        rg = self.route_geoms_repository.find_by_id(dto.route_geom_id)
        if not rg:
            raise ControlledException(route_geoms_error_code.ROUTE_GEOM_NOT_FOUND)

        # 화이트리스트 필드만 반영. 실수로 다른 속성 들어오는 것 차단.
        allowed = {"route_id", "geom"}
        data = dto.model_dump(exclude_none=True)
        for k, v in data.items():
            if k in allowed and k != "route_geom_id":
                if k == "geom":
                    setattr(rg, "geom", self._coerce_geom_input(v))
                else:
                    setattr(rg, k, v)

        try:
            self.database.commit()
        except IntegrityError as e:
            self.database.rollback()
            # 갱신 중 중복/제약 위반도 동일하게 매핑
            raise ControlledException(route_geoms_error_code.DUPLICATE_KEY) from e
        self.database.refresh(rg)
        return self._to_out(rg)

    # 삭제
    def delete_route_geom_by_id(self, route_geom_id: int) -> RouteGeomOut:
        rg = self.route_geoms_repository.find_by_id(route_geom_id)
        if not rg:
            raise ControlledException(route_geoms_error_code.ROUTE_GEOM_NOT_FOUND)
        # 삭제 전 직렬화 뽑아두기
        out = self._to_out(rg)
        self.route_geoms_repository.delete(rg)
        self.database.commit()  # delete는 커밋까지 해야 반영
        return out
