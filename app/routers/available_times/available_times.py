# app/routers/available_times/available_times.py
from sqlalchemy import Column, Integer, Identity, DateTime, func, Boolean, text, ForeignKey

from config.database.postgres_database import Base


class AvailableTimes(Base):
    """
    러닝 경로(route)에 대해 사용자가 이용 가능한 시간대를 저장하는 테이블.

    - route_id: 대상 Route의 FK
    - since: 이 가용 시간이 적용되기 시작한 시점(버전/정책 개시일 느낌)
    - start_time: 실제 이용 가능 시작 시각(타임존 포함)
    - end_time: 실제 이용 가능 종료 시각(타임존 포함)
    - is_deleted: 소프트 삭제 플래그
    - created_at: 생성 시각
    - updated_at: 갱신 시각
    """
    __tablename__ = "available_times"

    available_time_id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    route_id = Column(Integer, ForeignKey("routes.route_id", ondelete="CASCADE"), nullable=False)

    since = Column(DateTime(timezone=True), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)

    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())