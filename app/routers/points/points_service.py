# app/routers/points/points_service.py
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.internal.exception.controlled_exception import ControlledException
from app.internal.exception.errorcode import points_error_code
from app.routers.points.points import Points
from app.routers.points.points_dto import PointCreate, PointUpdate
from app.routers.points.points_repository import PointsRepository

class PointsService:
    def __init__(self, database: Session, points_repository: PointsRepository) -> None:
        # Service는 트랜잭션 경계(Commit/Rollback) + 의미있는 예외 매핑 담당.
        self.database = database
        self.points_repository = points_repository

    # 생성
    def create_point(self, point_create: PointCreate) -> Points:
        point = Points(
            section_id=point_create.section_id,
            index=point_create.index,
            distance=point_create.distance,
            latitude=point_create.latitude,
            longitude=point_create.longitude,
            height=point_create.height,
        )
        try:
            self.points_repository.save(point)   # flush까지 하고 PK 확보
            self.database.commit()               # 트랜잭션 확정은 Service에서만
        except IntegrityError as e:
            self.database.rollback()
            # FK/유니크 위반 등 → 비즈니스 에러코드로 변환
            raise ControlledException(points_error_code.DUPLICATE_KEY) from e

        self.database.refresh(point)            # server_default/trigger 동기화
        return point

    # 조회 (없으면 예외)
    def find_by_id(self, point_id: int) -> Points:
        point = self.points_repository.find_by_id(point_id)
        if not point:
            raise ControlledException(points_error_code.POINT_NOT_FOUND)
        return point

    def find_all(self) -> List[Points]:
        points = self.points_repository.find_all()
        if not points:
            # 빈 리스트를 허용하고 싶다면 이 예외를 제거하세요.
            raise ControlledException(points_error_code.POINT_NOT_FOUND)
        return points

    def find_by_section_id(self, section_id: int) -> List[Points]:
        points = self.points_repository.find_by_section_id(section_id)
        if not points:
            raise ControlledException(points_error_code.POINT_NOT_FOUND)
        return points

    # 갱신
    def update_point(self, point_update: PointUpdate) -> Points:
        point = self.points_repository.find_by_id(point_update.point_id)
        if not point:
            raise ControlledException(points_error_code.POINT_NOT_FOUND)

        # 화이트리스트 필드만 반영
        allowed = {"section_id", "index", "distance", "latitude", "longitude", "height", "is_deleted"}
        data = point_update.model_dump(exclude_none=True)
        for k, v in data.items():
            if k in allowed and k != "point_id":
                setattr(point, k, v)

        try:
            self.database.commit()
        except IntegrityError as e:
            self.database.rollback()
            raise ControlledException(points_error_code.DUPLICATE_KEY) from e
        self.database.refresh(point)
        return point

    # 삭제
    def delete_point_by_id(self, point_id: int) -> Points:
        point = self.points_repository.find_by_id(point_id)
        if not point:
            raise ControlledException(points_error_code.POINT_NOT_FOUND)
        self.points_repository.delete(point)
        self.database.commit()
        return point
