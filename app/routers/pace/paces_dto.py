from pydantic import BaseModel


class PaceBase(BaseModel):
    message: str