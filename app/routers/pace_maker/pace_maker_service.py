# app/routers/pace_records/pace_records_service.py
from app.routers.pace_maker.pace_maker_dto import PaceMakerDTO
from config.llm.pace_maker_llm import PaceMakerLLM


class PaceMakerService:
    def pace_maker(self, pace_base:PaceMakerDTO):
        print(pace_base)
        print(pace_base.model_dump_json())
        return PaceMakerLLM().invoke({"input": pace_base})
