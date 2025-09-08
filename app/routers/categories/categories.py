# app/routers/categories/categories.py
from sqlalchemy import Column, Integer, Identity, ForeignKey, String, Boolean, DateTime, text, func, UniqueConstraint
from config.database.postgres_database import Base

class Categories(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    name = Column(String(255), nullable=False)

    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # 한 유저 내 동일 이름 금지
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_categories_user_name"),
    )