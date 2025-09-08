# app/routers/pace_records/pace_records_service.py
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.internal.exception.controlled_exception import ControlledException
from app.internal.exception.errorcode import pace_records_error_code
from app.routers.pace_records.pace_records import PaceRecords
from app.routers.pace_records.pace_records_dto import PaceRecordCreate, PaceRecordUpdate
from app.routers.pace_records.pace_records_repository import PaceRecordsRepository

class PaceRecordsService:
    def __init__(self, database: Session, repository: PaceRecordsRepository) -> None:
        self.database = database
        self.repository = repository

    def create_pace_record(self, dto: PaceRecordCreate) -> PaceRecords:
        item = PaceRecords(record_id=dto.record_id, section_id=dto.section_id, pace=dto.pace)
        try:
            self.repository.save(item)
            self.database.commit()
        except IntegrityError as e:
            self.database.rollback()
            raise ControlledException(pace_records_error_code.DUPLICATE_KEY) from e
        self.database.refresh(item)
        return item

    def find_by_id(self, pace_record_id: int) -> PaceRecords:
        item = self.repository.find_by_id(pace_record_id)
        if not item:
            raise ControlledException(pace_records_error_code.PACE_RECORD_NOT_FOUND)
        return item

    def find_all(self) -> List[PaceRecords]:
        rows = self.repository.find_all()
        if not rows:
            raise ControlledException(pace_records_error_code.PACE_RECORD_NOT_FOUND)
        return rows

    def find_by_record_id(self, record_id: int) -> List[PaceRecords]:
        rows = self.repository.find_by_record_id(record_id)
        if not rows:
            raise ControlledException(pace_records_error_code.PACE_RECORD_NOT_FOUND)
        return rows

    def update_pace_record(self, dto: PaceRecordUpdate) -> PaceRecords:
        item = self.repository.find_by_id(dto.pace_record_id)
        if not item:
            raise ControlledException(pace_records_error_code.PACE_RECORD_NOT_FOUND)
        allowed = {"record_id", "section_id", "pace"}
        data = dto.model_dump(exclude_none=True)
        for k, v in data.items():
            if k in allowed and k != "pace_record_id":
                setattr(item, k, v)
        try:
            self.database.commit()
        except IntegrityError as e:
            self.database.rollback()
            raise ControlledException(pace_records_error_code.DUPLICATE_KEY) from e
        self.database.refresh(item)
        return item

    def delete_pace_record_by_id(self, pace_record_id: int) -> PaceRecords:
        item = self.repository.find_by_id(pace_record_id)
        if not item:
            raise ControlledException(pace_records_error_code.PACE_RECORD_NOT_FOUND)
        self.repository.delete(item)
        self.database.commit()
        return item
