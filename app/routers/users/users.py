from sqlalchemy import Column, Integer, Identity, String, Boolean, DateTime, text
from sqlalchemy.sql import func
from config.database.postgres_database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)  # SQLAlchemy String
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # 해시 저장 권장
    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
