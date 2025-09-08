# app/routers/routes/routes_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.routers.routes.routes import Routes

class RoutesRepository:
    def __init__(self, database: Session) -> None:
        # Repository는 DB 접근 전용. 트랜잭션(Commit/Rollback) 모름.
        self.database = database

    # 트랜잭션은 Service가 관리 → 여기선 commit() 하지 않음
    def save(self, route: Routes) -> Routes:
        # add로 pending에 올리고, flush로 즉시 INSERT 실행 + PK 확보.
        self.database.add(route)
        self.database.flush() # PK 확보/조기 예외 감지
        return route

    def find_by_id(self, route_id: int) -> Optional[Routes]:
        # PK 조회 최단코스. 없으면 None.
        return self.database.get(Routes, route_id)

    def find_all(self) -> List[Routes]:
        # 전체 조회. scalars()로 엔티티 컬럼만 뽑고, all() → list 캐스팅.
        return list(self.database.execute(select(Routes)).scalars().all())

    def delete(self, route: Routes) -> None:
        # 삭제는 Service에서 commit으로 마무리.
        self.database.delete(route)
