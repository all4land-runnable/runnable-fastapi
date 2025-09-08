# app/routers/ranks/ranks_service.py
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.internal.exception.controlled_exception import ControlledException
from app.internal.exception.errorcode import ranks_error_code
from app.routers.ranks.ranks import Ranks
from app.routers.ranks.ranks_dto import RankCreate, RankUpdate
from app.routers.ranks.ranks_repository import RanksRepository

class RanksService:
    def __init__(self, database: Session, repository: RanksRepository) -> None:
        self.database = database
        self.repository = repository

    def create_rank(self, dto: RankCreate) -> Ranks:
        item = Ranks(record_id=dto.record_id, rank=dto.rank)
        try:
            self.repository.save(item)
            self.database.commit()
        except IntegrityError as e:
            self.database.rollback()
            raise ControlledException(ranks_error_code.DUPLICATE_KEY) from e
        self.database.refresh(item)
        return item

    def find_by_id(self, rank_id: int) -> Ranks:
        item = self.repository.find_by_id(rank_id)
        if not item:
            raise ControlledException(ranks_error_code.RANK_NOT_FOUND)
        return item

    def find_all(self) -> List[Ranks]:
        rows = self.repository.find_all()
        if not rows:
            raise ControlledException(ranks_error_code.RANK_NOT_FOUND)
        return rows

    def find_by_record_id(self, record_id: int) -> List[Ranks]:
        rows = self.repository.find_by_record_id(record_id)
        if not rows:
            raise ControlledException(ranks_error_code.RANK_NOT_FOUND)
        return rows

    def update_rank(self, dto: RankUpdate) -> Ranks:
        item = self.repository.find_by_id(dto.rank_id)
        if not item:
            raise ControlledException(ranks_error_code.RANK_NOT_FOUND)
        allowed = {"record_id", "rank"}
        data = dto.model_dump(exclude_none=True)
        for k, v in data.items():
            if k in allowed and k != "rank_id":
                setattr(item, k, v)
        try:
            self.database.commit()
        except IntegrityError as e:
            self.database.rollback()
            raise ControlledException(ranks_error_code.DUPLICATE_KEY) from e
        self.database.refresh(item)
        return item

    def delete_rank_by_id(self, rank_id: int) -> Ranks:
        item = self.repository.find_by_id(rank_id)
        if not item:
            raise ControlledException(ranks_error_code.RANK_NOT_FOUND)
        self.repository.delete(item)
        self.database.commit()
        return item
