# app/routers/points/points.py
from sqlalchemy import Column, Integer, Identity, ForeignKey, Float, Boolean, DateTime, text, func

from config.database.postgres_database import Base


class Points(Base):
    __tablename__ = "points"

    point_id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    section_id = Column(Integer, ForeignKey("sections.section_id", ondelete="CASCADE"), nullable=False)

    index = Column(Integer, nullable=False)
    distance = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    height = Column(Float, nullable=False)

    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())