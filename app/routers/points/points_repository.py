# app/routers/points/points_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.routers.points.points import Points

class PointsRepository:
    def __init__(self, database: Session) -> None:
        # Repository는 DB 접근 전용. 트랜잭션(Commit/Rollback) 모름.
        self.database = database

    # 트랜잭션은 Service가 관리 → 여기선 commit() 하지 않음
    def save(self, point: Points) -> Points:
        # add로 pending에 올리고, flush로 즉시 INSERT 실행 + PK 확보.
        self.database.add(point)
        self.database.flush()  # PK 확보/조기 예외 감지
        return point

    def find_by_id(self, point_id: int) -> Optional[Points]:
        # PK 조회 최단코스. 없으면 None.
        return self.database.get(Points, point_id)

    def find_all(self) -> List[Points]:
        # 전체 조회(소프트 삭제 제외). index ASC, point_id ASC 정렬.
        stmt = (
            select(Points)
            .where(Points.is_deleted.is_(False))
            .order_by(Points.index.asc(), Points.point_id.asc())
        )
        return list(self.database.execute(stmt).scalars().all())

    def find_by_section_id(self, section_id: int) -> List[Points]:
        # 특정 section에 속한 포인트들(소프트 삭제 제외)
        stmt = (
            select(Points)
            .where(
                Points.section_id == section_id,
                Points.is_deleted.is_(False),
            )
            .order_by(Points.index.asc(), Points.point_id.asc())
        )
        return list(self.database.execute(stmt).scalars().all())

    def delete(self, point: Points) -> None:
        # 삭제는 Service에서 commit으로 마무리.
        self.database.delete(point)

    def delete_by_id(self, point_id: int) -> bool:
        # 편의용. True면 삭제 예정 상태, 커밋은 Service에서.
        point = self.find_by_id(point_id)
        if not point:
            return False
        self.database.delete(point)
        return True
