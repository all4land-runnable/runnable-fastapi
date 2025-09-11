# app/routers/pace_maker/pace_maker.py
from pydantic import BaseModel

class Section(BaseModel):
    distance: float
    slope: float
    pace: float

class Route(BaseModel):
    sections: list[Section]

class PaceMakerDTO(BaseModel):
    luggageWeight: float
    paceSeconds: int
    route: Route