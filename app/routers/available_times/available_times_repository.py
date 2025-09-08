# app/routers/available_times/available_times_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.routers.available_times.available_times import AvailableTimes

class AvailableTimesRepository:
    def __init__(self, database: Session) -> None:
        # Repository는 DB 접근 전용. 트랜잭션(Commit/Rollback) 모름.
        self.database = database

    # 트랜잭션은 Service가 관리 → 여기선 commit() 하지 않음
    def save(self, item: AvailableTimes) -> AvailableTimes:
        # add로 pending에 올리고, flush로 즉시 INSERT 실행 + PK 확보.
        self.database.add(item)
        self.database.flush()   # PK 확보/조기 예외 감지
        return item

    def find_by_id(self, available_time_id: int) -> Optional[AvailableTimes]:
        # PK 조회 최단코스. 없으면 None.
        return self.database.get(AvailableTimes, available_time_id)

    def find_all(self) -> List[AvailableTimes]:
        # 전체 조회. scalars()로 엔티티 컬럼만 뽑고, all() → list 캐스팅.
        return list(self.database.execute(select(AvailableTimes)).scalars().all())

    def find_by_route_id(self, route_id: int) -> List[AvailableTimes]:
        # route 단위로 여러 건 가능
        return list(
            self.database.execute(
                select(AvailableTimes).where(AvailableTimes.route_id == route_id)
            ).scalars().all()
        )

    def delete(self, item: AvailableTimes) -> None:
        # 삭제는 Service에서 commit으로 마무리.
        self.database.delete(item)

    def delete_by_id(self, available_time_id: int) -> bool:
        # 편의용. True면 삭제 예정 상태, 커밋은 Service에서.
        item = self.find_by_id(available_time_id)
        if not item:
            return False
        self.database.delete(item)
        return True
