# app/routers/routes/routes.py
from sqlalchemy import Column, Integer, Identity, String, Boolean, DateTime, text, func, Float

from config.database.postgres_database import Base


class Routes(Base):
    __tablename__ = "routes"

    route_id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)

    high_height = Column(Float, nullable=False)
    low_height = Column(Float, nullable=False)
    distance = Column(Integer, nullable=False)
    pace = Column(Integer, nullable=False)

    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
