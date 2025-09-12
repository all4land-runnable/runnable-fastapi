from pydantic import BaseModel


class Section(BaseModel):
    distance: float
    slope: float
    startPlace: str
    pace: float | None = None
    strategies: list[str] | None = None

class Route(BaseModel):
    luggageWeight: float
    paceSeconds: int
    sections: list[Section]