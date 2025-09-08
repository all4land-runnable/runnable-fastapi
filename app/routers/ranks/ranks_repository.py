# app/routers/ranks/ranks_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
# 모델이 class ranks 로 정의되었다면 alias로 불러온다.
from app.routers.ranks.ranks import Ranks

class RanksRepository:
    def __init__(self, database: Session) -> None:
        self.database = database

    def save(self, item: Ranks) -> Ranks:
        self.database.add(item)
        self.database.flush()
        return item

    def find_by_id(self, rank_id: int) -> Optional[Ranks]:
        return self.database.get(Ranks, rank_id)

    def find_all(self) -> List[Ranks]:
        return list(self.database.execute(select(Ranks)).scalars().all())

    def find_by_record_id(self, record_id: int) -> List[Ranks]:
        stmt = select(Ranks).where(Ranks.record_id == record_id)
        return list(self.database.execute(stmt).scalars().all())

    def delete(self, item: Ranks) -> None:
        self.database.delete(item)
