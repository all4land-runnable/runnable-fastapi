# app/routers/route_geoms/route_geoms_dto.py
from pydantic import BaseModel, ConfigDict
from typing import Optional

# 공통 입력 필드
class RouteGeomBase(BaseModel):
    route_id: int
    geom: str

# 생성용 입력 DTO
class RouteGeomCreate(RouteGeomBase):
    pass

# 부분 수정용 DTO
class RouteGeomUpdate(BaseModel):
    route_geom_id: int
    route_id: Optional[int] = None
    geom: Optional[str] = None

# 출력용 DTO
class RouteGeomOut(RouteGeomBase):
    route_geom_id: int
    model_config = ConfigDict(from_attributes=True)
