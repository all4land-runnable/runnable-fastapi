from sqlalchemy import Column, Integer, Identity, ForeignKey, Text

from config.database.postgres_database import Base


class RouteGeoms(Base):
    __tablename__ = "route_geoms"

    route_geom_id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    route_id = Column(Integer, ForeignKey('routes.route_id', ondelete="CASCADE"), nullable=False)

    geom = Column(Text, nullable=False) # TODO 타입 수정
