# app/routers/available_times/available_times_service.py
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.internal.exception.controlled_exception import ControlledException
from app.internal.exception.errorcode import available_time_error_code
from app.routers.available_times.available_times import AvailableTimes
from app.routers.available_times.available_times_dto import AvailableTimeCreate, AvailableTimeUpdate
from app.routers.available_times.available_times_repository import AvailableTimesRepository

class AvailableTimesService:
    def __init__(self, database: Session, repository: AvailableTimesRepository) -> None:
        # Service는 트랜잭션 경계(Commit/Rollback) + 의미있는 예외 매핑 담당.
        self.database = database
        self.repository = repository

    # 생성
    def create_available_time(self, dto: AvailableTimeCreate) -> AvailableTimes:
        item = AvailableTimes(
            route_id=dto.route_id,
            since=dto.since,
            start_time=dto.start_time,
            end_time=dto.end_time,
        )
        try:
            self.repository.save(item)    # flush까지 하고 PK 확보
            self.database.commit()        # [핵심] 트랜잭션 확정은 Service에서만
        except IntegrityError as e:
            self.database.rollback()
            # 유니크 위반 등 → 비즈니스 에러코드로 변환
            raise ControlledException(available_time_error_code.DUPLICATE_KEY) from e

        self.database.refresh(item)       # server_default/trigger 동기화
        return item

    # 조회 (없으면 예외)
    def find_by_id(self, available_time_id: int) -> AvailableTimes:
        item = self.repository.find_by_id(available_time_id)
        if not item:
            raise ControlledException(available_time_error_code.AVAILABLE_TIME_NOT_FOUND)
        return item

    def find_all(self) -> List[AvailableTimes]:
        items = self.repository.find_all()
        if not items:
            raise ControlledException(available_time_error_code.AVAILABLE_TIME_NOT_FOUND)
        return items

    def find_by_route_id(self, route_id: int) -> List[AvailableTimes]:
        items = self.repository.find_by_route_id(route_id)
        if not items:
            raise ControlledException(available_time_error_code.AVAILABLE_TIME_NOT_FOUND)
        return items

    # 갱신
    def update_available_time(self, dto: AvailableTimeUpdate) -> AvailableTimes:
        item = self.repository.find_by_id(dto.available_time_id)
        if not item:
            raise ControlledException(available_time_error_code.AVAILABLE_TIME_NOT_FOUND)

        # [명준 주석]
        # - 화이트리스트 필드만 반영. 실수로 다른 속성 들어오는 것 차단.
        allowed = {"route_id", "since", "start_time", "end_time", "is_deleted"}
        data = dto.model_dump(exclude_none=True)  # None 값들은 아예 제외
        for k, v in data.items():
            if k in allowed and k != "available_time_id":
                setattr(item, k, v)

        try:
            self.database.commit()
        except IntegrityError as e:
            self.database.rollback()
            # 갱신 중 유니크 위반도 동일하게 매핑
            raise ControlledException(available_time_error_code.DUPLICATE_KEY) from e
        self.database.refresh(item)
        return item

    # 삭제
    def delete_available_time_by_id(self, available_time_id: int) -> AvailableTimes:
        item = self.repository.find_by_id(available_time_id)
        if not item:
            raise ControlledException(available_time_error_code.AVAILABLE_TIME_NOT_FOUND)
        self.repository.delete(item)
        self.database.commit()  # delete는 커밋까지 해야 반영
        return item
