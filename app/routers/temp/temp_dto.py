from pydantic import BaseModel


class TempBase(BaseModel):
    message: str