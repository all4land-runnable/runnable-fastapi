from sqlalchemy import Column, Integer, Identity, ForeignKey, String, Float

from config.database.postgres_database import Base


class UserPaces(Base):
    __tablename__ = "user_paces"

    user_pace_id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    user_strategy_id = Column(Integer, ForeignKey("strategies.strategy_id", ondelete="CASCADE"))
    section_id = Column(Integer, ForeignKey("sections.section_id", ondelete="CASCADE"))

    pace = Column(Integer, nullable=False)
    strategy = Column(String(255), nullable=False)
    foundation_latitude = Column(Float, nullable=False)
    foundation_longitude = Column(Float, nullable=False)
