from pydantic import BaseModel


class SlopeDatum(BaseModel):
    meter: float
    height: float
    slope: float
    pace: int | None