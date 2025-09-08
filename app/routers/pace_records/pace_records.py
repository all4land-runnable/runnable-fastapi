# app/routers/pace_records/pace_records.py
from sqlalchemy import ForeignKey, Column, Integer, Identity

from config.database.postgres_database import Base


class PaceRecords(Base):
    __tablename__ = "pace_records"

    pace_record_id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    record_id = Column(Integer, ForeignKey("records.record_id", ondelete="CASCADE"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.section_id", ondelete="CASCADE"))

    pace = Column(Integer, nullable=False)