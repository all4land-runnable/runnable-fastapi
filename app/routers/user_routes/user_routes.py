# app/routers/user_routes/user_routes.py
from sqlalchemy import Column, Integer, ForeignKey, Identity, Boolean, DateTime, text, func, UniqueConstraint
from config.database.postgres_database import Base

class UserRoutes(Base):
    __tablename__ = "user_routes"

    user_route_id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id", ondelete="CASCADE"), nullable=False)
    route_id = Column(Integer, ForeignKey("routes.route_id", ondelete="CASCADE"), nullable=False)

    # 메타 필드 (다른 엔티티와 동일)
    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # 동일 유저/카테고리에 같은 루트 중복 방지
    __table_args__ = (
        UniqueConstraint("user_id", "category_id", "route_id", name="uq_user_routes_triplet"),
    )
