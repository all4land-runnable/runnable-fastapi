# app/routers/user_paces/user_paces.py
from sqlalchemy import Column, Integer, Identity, ForeignKey, String, Float
from config.database.postgres_database import Base

class UserPaces(Base):
    __tablename__ = "user_paces"

    user_pace_id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    user_strategy_id = Column(Integer, ForeignKey("user_strategies.user_strategy_id", ondelete="CASCADE"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.section_id", ondelete="CASCADE"), nullable=False)

    pace = Column(Integer, nullable=False)  # 초 단위
    strategy = Column(String(255), nullable=False)
    foundation_latitude = Column(Float, nullable=False)
    foundation_longitude = Column(Float, nullable=False)
