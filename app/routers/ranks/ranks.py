# app/routers/ranks/ranks.py
from sqlalchemy import Column, Integer, ForeignKey, Identity

from config.database.postgres_database import Base


class Ranks(Base):
    __tablename__ = "ranks"

    rank_id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    record_id = Column(Integer, ForeignKey("records.record_id", ondelete="CASCADE"))

    rank = Column(Integer, nullable=False)