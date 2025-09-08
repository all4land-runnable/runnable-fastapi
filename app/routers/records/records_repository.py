# app/routers/records/records_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.routers.records.records import Records

class RecordsRepository:
    def __init__(self, database: Session) -> None:
        # Repository는 DB 접근 전용. 트랜잭션(Commit/Rollback) 모름.
        self.database = database

    # 트랜잭션은 Service가 관리 → 여기선 commit() 하지 않음
    def save(self, rec: Records) -> Records:
        # add로 pending에 올리고, flush로 즉시 INSERT 실행 + PK 확보.
        self.database.add(rec)
        self.database.flush()   # PK 확보/조기 예외 감지
        return rec

    def find_by_id(self, record_id: int) -> Optional[Records]:
        # PK 조회 최단코스. 없으면 None.
        return self.database.get(Records, record_id)

    def find_all(self) -> List[Records]:
        # 전체 조회. scalars()로 엔티티 컬럼만 뽑고, all() → list 캐스팅.
        return list(self.database.execute(select(Records)).scalars().all())

    def find_by_user_route_id(self, user_route_id: int) -> List[Records]:
        # 동일 user_route에 여러 기록이 있을 수 있음
        stmt = select(Records).where(Records.user_route_id == user_route_id)
        return list(self.database.execute(stmt).scalars().all())

    def delete(self, rec: Records) -> None:
        # 삭제는 Service에서 commit으로 마무리.
        self.database.delete(rec)

    def delete_by_id(self, record_id: int) -> bool:
        rec = self.find_by_id(record_id)
        if not rec:
            return False
        self.database.delete(rec)
        return True
