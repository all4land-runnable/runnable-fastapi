# app/routers/sections/sections_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.routers.sections.sections import Sections


class SectionsRepository:
    def __init__(self, database: Session) -> None:
        # Repository는 DB 접근 전용. 트랜잭션(Commit/Rollback) 모름.
        self.database = database

    # 트랜잭션은 Service가 관리 → 여기선 commit() 하지 않음
    def save(self, section: Sections) -> Sections:
        # add로 pending에 올리고, flush로 즉시 INSERT 실행 + PK 확보.
        self.database.add(section)
        self.database.flush()   # PK 확보/조기 예외 감지
        return section

    def find_by_id(self, section_id: int) -> Optional[Sections]:
        # PK 조회 최단코스. 없으면 None.
        return self.database.get(Sections, section_id)

    def find_all(self) -> List[Sections]:
        # 전체 조회. scalars()로 엔티티 컬럼만 뽑고, all() → list 캐스팅.
        return list(self.database.execute(select(Sections)).scalars().all())

    def find_by_route_id(self, route_id: int) -> List[Sections]:
        # 특정 route에 속한 섹션들
        stmt = select(Sections).where(Sections.route_id == route_id)
        return list(self.database.execute(stmt).scalars().all())

    def delete(self, section: Sections) -> None:
        # 삭제는 Service에서 commit으로 마무리.
        self.database.delete(section)

    def delete_by_id(self, section_id: int) -> bool:
        # 편의용. True면 삭제 예정 상태, 커밋은 Service에서.
        section = self.find_by_id(section_id)
        if not section:
            return False
        self.database.delete(section)
        return True
