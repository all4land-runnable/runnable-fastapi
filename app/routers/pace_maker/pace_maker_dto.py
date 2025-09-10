# app/routers/temp/temp_dto.py
from pydantic import BaseModel

class Section(BaseModel):
    distance: float
    slope: float

class Route(BaseModel):
    sections: list[Section]

class PaceMakerDTO(BaseModel):
    luggageWeight: float
    paceSeconds: int
    route: Route