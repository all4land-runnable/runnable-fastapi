from sqlalchemy.orm import Session

from app.routers.temp.temp_dto import TempBase
from config.llm.main_llm import main_llm


class TempService:
    def __init__(self, database: Session):
        self.database = database

    def chat(self, pace_base:TempBase)->dict:
        return main_llm.invoke({"input":pace_base.message})