from sqlalchemy import Identity, Column, Integer, ForeignKey, Float

from config.database.postgres_database import Base


class UserStrategies(Base):
    __tablename__ = "user_strategies"

    user_strategy_id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    user_route_id = Column(Integer, ForeignKey("routes.route_id", ondelete="CASCADE"), nullable=False)

    luggage_weight = Column(Integer, nullable=False)
    pace_average = Column(Integer, nullable=False) # 초단위로 저장