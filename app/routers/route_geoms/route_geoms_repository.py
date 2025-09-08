# app/routers/route_geoms/route_geoms_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.routers.route_geoms.route_geoms import RouteGeoms

class RouteGeomsRepository:
    def __init__(self, database: Session) -> None:
        # Repository는 DB 접근 전용. 트랜잭션(Commit/Rollback) 모름.
        self.database = database

    # 트랜잭션은 Service가 관리 → 여기선 commit() 하지 않음
    def save(self, route_geom: RouteGeoms) -> RouteGeoms:
        # add로 pending에 올리고, flush로 즉시 INSERT 실행 + PK 확보.
        self.database.add(route_geom)
        self.database.flush()   # PK 확보/조기 예외 감지
        return route_geom

    def find_by_id(self, route_geom_id: int) -> Optional[RouteGeoms]:
        # PK 조회 최단코스. 없으면 None.
        return self.database.get(RouteGeoms, route_geom_id)

    def find_all(self) -> List[RouteGeoms]:
        # 전체 조회. scalars()로 엔티티 컬럼만 뽑고, all() → list 캐스팅.
        return list(self.database.execute(select(RouteGeoms)).scalars().all())

    def find_by_route_id(self, route_id: int) -> List[RouteGeoms]:
        # 특정 route의 지오메트리들
        stmt = select(RouteGeoms).where(RouteGeoms.route_id == route_id)
        return list(self.database.execute(stmt).scalars().all())

    def delete(self, route_geom: RouteGeoms) -> None:
        # 삭제는 Service에서 commit으로 마무리.
        self.database.delete(route_geom)

    def delete_by_id(self, route_geom_id: int) -> bool:
        # 편의용. True면 삭제 예정 상태, 커밋은 Service에서.
        rg = self.find_by_id(route_geom_id)
        if not rg:
            return False
        self.database.delete(rg)
        return True
