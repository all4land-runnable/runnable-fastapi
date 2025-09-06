from sqlalchemy.orm import Session

from app.routers.pace.paces_dto import PaceBase
from config.llm.main_llm import main_llm


class PacesService:
    def __init__(self, database: Session):
        self.database = database

    def chat(self, pace_base:PaceBase)->dict:
        return main_llm.invoke({"input":pace_base.message})