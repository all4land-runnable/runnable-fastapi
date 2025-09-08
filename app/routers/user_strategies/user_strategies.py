# app/routers/user_strategies/user_strategies.py
from sqlalchemy import Column, Integer, Identity, ForeignKey, Boolean, DateTime, text, func, UniqueConstraint
from config.database.postgres_database import Base

class UserStrategies(Base):
    __tablename__ = "user_strategies"

    user_strategy_id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    user_route_id = Column(Integer, ForeignKey("user_routes.user_route_id", ondelete="CASCADE"), nullable=False)

    luggage_weight = Column(Integer, nullable=False)
    pace_average = Column(Integer, nullable=False)  # 초단위로 저장

    # 메타 필드 (다른 엔티티와 동일)
    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # 한 user_route 당 전략은 1개만 허용
    __table_args__ = (
        UniqueConstraint("user_route_id", name="uq_user_strategies_user_route"),
    )
