# app/routers/available_times/available_times.py
from sqlalchemy import Column, Integer, Identity, DateTime, func, Boolean, text, ForeignKey

from config.database.postgres_database import Base


class AvailableTimes(Base):
    __tablename__ = "available_times"

    available_time_id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    route_id = Column(Integer, ForeignKey("routes.route_id", ondelete="CASCADE"), nullable=False)

    since = Column(DateTime(timezone=True), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)

    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())