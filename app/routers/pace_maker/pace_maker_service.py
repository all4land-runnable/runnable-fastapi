# app/routers/pace_records/pace_records_service.py
from app.routers.pace_maker.pace_maker import Route
from config.llm.pace_maker_llm import PaceMakerLLM


class PaceMakerService:
    def pace_maker(self, route:Route):
        return PaceMakerLLM().invoke({"input": route})
