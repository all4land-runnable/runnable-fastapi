# app/routers/pace_maker/pace_maker.py
from pydantic import BaseModel

class Section(BaseModel):
    distance: float
    slope: float
    pace: float
    startPlace: str
    strategies: str

class Route(BaseModel):
    luggageWeight: float
    paceSeconds: int
    sections: list[Section]