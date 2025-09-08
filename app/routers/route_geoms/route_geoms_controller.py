# app/routers/route_geoms/route_geoms_controller.py
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from app.routers.route_geoms.route_geoms_dto import RouteGeomCreate, RouteGeomUpdate, RouteGeomOut
from app.routers.route_geoms.route_geoms_repository import RouteGeomsRepository
from app.routers.route_geoms.route_geoms_service import RouteGeomsService
from config.common.common_response import CommonResponse
from config.database.postgres_database import get_database  # Session 제공

router = APIRouter(prefix="/route-geoms", tags=["route_geoms"])

# - 여기서 Service 인스턴스를 DI로 주입한다.
# - 포인트: 라우터는 비즈니스 로직 모름. 의존성으로 Service만 받아서 호출.
# - Session은 요청 단위로 열고 닫힘(get_database). 메모리 누수 방지.
def get_route_geoms_service(database: Session = Depends(get_database)) -> RouteGeomsService:
    repo = RouteGeomsRepository(database)               # Repository는 트랜잭션 모름(Commit 금지)
    return RouteGeomsService(database, repo)            # Service가 트랜잭션/예외 관리 담당

# 생성
@router.post(
    "",
    response_model=CommonResponse[RouteGeomOut],
    status_code=status.HTTP_201_CREATED,
)
def create_route_geom(dto: RouteGeomCreate, svc: RouteGeomsService = Depends(get_route_geoms_service)):
    rg = svc.create_route_geom(dto)
    return CommonResponse(code=201, message="경로 지오메트리 생성 성공", data=rg)

# 수정
@router.patch(
    "",
    response_model=CommonResponse[RouteGeomOut],
    status_code=status.HTTP_200_OK,
)
def update_route_geom(dto: RouteGeomUpdate, svc: RouteGeomsService = Depends(get_route_geoms_service)):
    rg = svc.update_route_geom(dto)
    return CommonResponse(code=200, message="경로 지오메트리 수정 성공", data=rg)

# 삭제
@router.delete(
    "/{route_geom_id}",
    response_model=CommonResponse[RouteGeomOut],
    status_code=status.HTTP_200_OK,
)
def delete_route_geom(route_geom_id: int, svc: RouteGeomsService = Depends(get_route_geoms_service)):
    rg = svc.delete_route_geom_by_id(route_geom_id)
    return CommonResponse(code=200, message="경로 지오메트리 삭제 성공", data=rg)

# 전체 조회
@router.get(
    "",
    response_model=CommonResponse[list[RouteGeomOut]],
    status_code=status.HTTP_200_OK,
)
def get_all(svc: RouteGeomsService = Depends(get_route_geoms_service)):
    rgs = svc.find_all()
    return CommonResponse(code=200, message="경로 지오메트리 전체 조회 성공", data=rgs)

# route_id로 조회
@router.get(
    "/route/{route_id}",
    response_model=CommonResponse[list[RouteGeomOut]],
    status_code=status.HTTP_200_OK,
)
def read_by_route_id(route_id: int, svc: RouteGeomsService = Depends(get_route_geoms_service)):
    rgs = svc.find_by_route_id(route_id)
    return CommonResponse(code=200, message="경로 지오메트리 조회 성공", data=rgs)

# 개별 조회
@router.get(
    "/{route_geom_id}",
    response_model=CommonResponse[RouteGeomOut],
    status_code=status.HTTP_200_OK,
)
def read_by_id(route_geom_id: int, svc: RouteGeomsService = Depends(get_route_geoms_service)):
    rg = svc.find_by_id(route_geom_id)
    return CommonResponse(code=200, message="경로 지오메트리 조회 성공", data=rg)
