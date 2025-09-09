# app/routers/temp/temp2_service.py
from sqlalchemy.orm import Session

from app.routers.temp.temp_dto import TempBase
from app.routers.temp2.temp2_llm import PaceLLM2


class Temp2Service:
    def __init__(self, database: Session):
        self.database = database

    def create_paces2(self, pace_base:TempBase):
        print(pace_base)
        print(pace_base.model_dump_json())
        return PaceLLM2().invoke({"input": pace_base})