from sqlalchemy import Column, Integer, ForeignKey, Identity

from config.database.postgres_database import Base


class UserRoutes(Base):
    __tablename__ = "user_routes"

    user_route_id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id", ondelete="CASCADE"), nullable=False)
    route_id = Column(Integer, ForeignKey("routes.route_id", ondelete="CASCADE"), nullable=False)