# app/routers/sections/sections.py
from sqlalchemy import Column, Integer, Identity, Boolean, DateTime, text, func, Float, ForeignKey, String
from config.database.postgres_database import Base

class Sections(Base):
    __tablename__ = "sections"

    section_id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    route_id = Column(Integer, ForeignKey("routes.route_id", ondelete="CASCADE"), nullable=False)

    start_place = Column(String(255), nullable=False)
    strategies = Column(String(255), nullable=False)
    distance = Column(Float, nullable=False)
    slope = Column(Float, nullable=False)
    pace = Column(Integer, nullable=False)

    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
