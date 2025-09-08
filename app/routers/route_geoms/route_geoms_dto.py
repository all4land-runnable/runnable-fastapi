# app/routers/route_geoms/route_geoms_dto.py
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

# 공통 입력 필드
class RouteGeomBase(BaseModel):
    route_id: int = Field(
        ...,
        description="지오메트리가 속한 경로 ID(PK).",
        examples=[101],
    )
    geom: str = Field(
        ...,
        description=(
            "경로 지오메트리 문자열. 현재는 텍스트로 수신하며 WKT(권장) 또는 GeoJSON 문자열을 허용합니다. "
            '예: WKT `"LINESTRING(127.1000 37.5000, 127.1100 37.5100)"`'
        ),
        examples=['LINESTRING(127.1000 37.5000, 127.1100 37.5100)'],
    )

# 생성용 입력 DTO
class RouteGeomCreate(RouteGeomBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "route_id": 101,
                    "geom": "LINESTRING(127.1000 37.5000, 127.1100 37.5100)",
                }
            ]
        }
    )

# 부분 수정용 DTO
class RouteGeomUpdate(BaseModel):
    route_geom_id: int = Field(
        ...,
        description="수정할 지오메트리 레코드 ID(PK).",
        examples=[1001],
    )
    route_id: Optional[int] = Field(
        None,
        description="수정할 경로 ID.",
        examples=[102],
    )
    geom: Optional[str] = Field(
        None,
        description="수정할 지오메트리 문자열(WKT/GeoJSON).",
        examples=['LINESTRING(127.1200 37.5200, 127.1300 37.5300)'],
    )

# 출력용 DTO
class RouteGeomOut(RouteGeomBase):
    route_geom_id: int = Field(
        ...,
        description="지오메트리 레코드 ID(PK).",
        examples=[1001],
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "route_geom_id": 1001,
                    "route_id": 101,
                    "geom": "LINESTRING(127.1000 37.5000, 127.1100 37.5100)",
                }
            ]
        },
    )
