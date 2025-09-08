# app/routers/ranks/ranks_dto.py
from pydantic import BaseModel, ConfigDict
from typing import Optional

class RankBase(BaseModel):
    record_id: int
    rank: int

class RankCreate(RankBase):
    pass

class RankUpdate(BaseModel):
    rank_id: int
    record_id: Optional[int] = None
    rank: Optional[int] = None

class RankOut(RankBase):
    rank_id: int
    model_config = ConfigDict(from_attributes=True)
