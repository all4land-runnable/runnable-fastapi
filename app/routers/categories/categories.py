from sqlalchemy import Column, Integer, Identity, ForeignKey, String

from config.database.postgres_database import Base


class Categories(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    name = Column(String, nullable=False)