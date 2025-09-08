from sqlalchemy import Identity, Column, Integer, ForeignKey

from config.database.postgres_database import Base


class Records(Base):
    __tablename__ = "records"

    record_id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    user_route_id = Column(Integer, ForeignKey("user_routes.user_route_id", ondelete="CASCADE"))

    paces_average = Column(Integer, nullable=False)