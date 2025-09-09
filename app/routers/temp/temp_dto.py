# app/routers/temp/temp_dto.py
from pydantic import BaseModel

from app.routers.temp.temp import SlopeDatum


class TempBase(BaseModel):
    limitRange: float
    luggageWeight: float
    paceSeconds: int
    slopeDatum: list[SlopeDatum]
