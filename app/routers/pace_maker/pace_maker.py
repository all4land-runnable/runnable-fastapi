from pydantic import BaseModel, Field


class SlopeDatum(BaseModel):
    meter: float
    height: float
    slope: float