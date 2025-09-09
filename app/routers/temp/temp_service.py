# app/routers/temp/temp_service.py
from sqlalchemy.orm import Session

from app.routers.temp.temp_dto import TempBase
from config.llm.main_llm import main_llm


class TempService:
    def __init__(self, database: Session):
        self.database = database

    def create_paces(self, pace_base:TempBase)->dict:
        payload = pace_base.model_dump()
        return main_llm.invoke({"input": payload})