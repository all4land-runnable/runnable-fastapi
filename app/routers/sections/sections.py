# app/routers/sections/sections.py
from sqlalchemy import Column, Integer, Identity, ForeignKey, Float

from config.database.postgres_database import Base


class Sections(Base):
    __tablename__ = "sections"

    section_id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    route_id = Column(Integer, ForeignKey("routes.route_id", ondelete="CASCADE"), nullable=False)

    start_latitude = Column(Float, nullable=False)
    start_longitude = Column(Float, nullable=False)
    start_height = Column(Float, nullable=False)

    end_latitude = Column(Float, nullable=False)
    end_longitude = Column(Float, nullable=False)
    end_height = Column(Float, nullable=False)

    slope = Column(Integer, nullable=False) # TODO 타입 수정