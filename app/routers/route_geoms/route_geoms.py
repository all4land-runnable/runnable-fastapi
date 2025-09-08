# app/routers/route_geoms/route_geoms.py
from sqlalchemy import Column, Integer, Identity, ForeignKey
from geoalchemy2 import Geometry
from config.database.postgres_database import Base


class RouteGeoms(Base):
    __tablename__ = "route_geoms"

    route_geom_id = Column(Integer, Identity(start=1, always=False), primary_key=True)
    route_id = Column(Integer, ForeignKey('routes.route_id', ondelete="CASCADE"), nullable=False)

    # 라인 경로 가정. 필요 시 'GEOMETRY' 또는 다른 타입/차원으로 교체 가능
    # SRID는 WGS84(4326). PostGIS 설치 필요: CREATE EXTENSION IF NOT EXISTS postgis;
    geom = Column(Geometry(geometry_type="LINESTRING", srid=4326), nullable=False)
