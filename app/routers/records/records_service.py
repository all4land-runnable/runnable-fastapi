# app/routers/records/records_service.py
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.internal.exception.controlled_exception import ControlledException
from app.internal.exception.errorcode import records_error_code
from app.routers.records.records import Records
from app.routers.records.records_dto import RecordCreate, RecordUpdate
from app.routers.records.records_repository import RecordsRepository

class RecordsService:
    def __init__(self, database: Session, repository: RecordsRepository) -> None:
        # Service는 트랜잭션 경계(Commit/Rollback) + 의미있는 예외 매핑 담당.
        self.database = database
        self.repository = repository

    # 생성
    def create_record(self, dto: RecordCreate) -> Records:
        rec = Records(
            user_route_id=dto.user_route_id,
            paces_average=dto.paces_average,
        )
        try:
            self.repository.save(rec)    # flush까지 하고 PK 확보
            self.database.commit()       # [핵심] 트랜잭션 확정은 Service에서만
        except IntegrityError as e:
            self.database.rollback()
            # 유니크/참조 무결성 위반 → 비즈니스 에러코드로 변환
            raise ControlledException(records_error_code.DUPLICATE_KEY) from e

        self.database.refresh(rec)       # server_default/trigger 동기화
        return rec

    # 조회 (없으면 예외)
    def find_by_id(self, record_id: int) -> Records:
        rec = self.repository.find_by_id(record_id)
        if not rec:
            raise ControlledException(records_error_code.RECORD_NOT_FOUND)
        return rec

    def find_all(self) -> List[Records]:
        rows = self.repository.find_all()
        if not rows:
            raise ControlledException(records_error_code.RECORD_NOT_FOUND)
        return rows

    def find_by_user_route_id(self, user_route_id: int) -> List[Records]:
        rows = self.repository.find_by_user_route_id(user_route_id)
        if not rows:
            raise ControlledException(records_error_code.RECORD_NOT_FOUND)
        return rows

    # 갱신
    def update_record(self, dto: RecordUpdate) -> Records:
        rec = self.repository.find_by_id(dto.record_id)
        if not rec:
            raise ControlledException(records_error_code.RECORD_NOT_FOUND)

        # [명준 주석]
        # - 화이트리스트 필드만 반영. 실수로 다른 속성 들어오는 것 차단.
        allowed = {"user_route_id", "paces_average"}
        data = dto.model_dump(exclude_none=True)  # None 값들은 아예 제외
        for k, v in data.items():
            if k in allowed and k != "record_id":
                setattr(rec, k, v)

        try:
            self.database.commit()
        except IntegrityError as e:
            self.database.rollback()
            raise ControlledException(records_error_code.DUPLICATE_KEY) from e
        self.database.refresh(rec)
        return rec

    # 삭제
    def delete_record_by_id(self, record_id: int) -> Records:
        rec = self.repository.find_by_id(record_id)
        if not rec:
            raise ControlledException(records_error_code.RECORD_NOT_FOUND)
        self.repository.delete(rec)
        self.database.commit()  # delete는 커밋까지 해야 반영
        return rec
