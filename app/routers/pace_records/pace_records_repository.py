# app/routers/pace_records/pace_records_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.routers.pace_records.pace_records import PaceRecords

class PaceRecordsRepository:
    def __init__(self, database: Session) -> None:
        self.database = database

    def save(self, item: PaceRecords) -> PaceRecords:
        self.database.add(item)
        self.database.flush()
        return item

    def find_by_id(self, pace_record_id: int) -> Optional[PaceRecords]:
        return self.database.get(PaceRecords, pace_record_id)

    def find_all(self) -> List[PaceRecords]:
        return list(self.database.execute(select(PaceRecords)).scalars().all())

    def find_by_record_id(self, record_id: int) -> List[PaceRecords]:
        stmt = select(PaceRecords).where(PaceRecords.record_id == record_id)
        return list(self.database.execute(stmt).scalars().all())

    def delete(self, item: PaceRecords) -> None:
        self.database.delete(item)
