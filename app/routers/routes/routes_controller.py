# app/routers/routes/routes_controller.py
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from app.routers.routes.routes_dto import RouteCreate, RouteUpdate, RouteDelete, RouteOut
from app.routers.routes.routes_repository import RoutesRepository
from app.routers.routes.routes_service import RoutesService
from config.common.common_response import CommonResponse
from config.database.postgres_database import get_database  # Session 제공

router = APIRouter(prefix="/routes", tags=["routes"])

# - 여기서 Service 인스턴스를 DI로 주입한다.
# - 포인트: 라우터는 비즈니스 로직 모름. 의존성으로 Service만 받아서 호출.
# - Session은 요청 단위로 열고 닫힘(get_database). 메모리 누수 방지.
def get_routes_service(database: Session = Depends(get_database)) -> RoutesService:
    routes_repository = RoutesRepository(database)            # Repository는 트랜잭션 모름(Commit 금지)
    return RoutesService(database, routes_repository)         # Service가 트랜잭션/예외 관리 담당

# 생성
@router.post(
    "",
    response_model=CommonResponse[RouteOut],
    status_code=status.HTTP_201_CREATED,
)
def create_route(route_create: RouteCreate, routes_service: RoutesService = Depends(get_routes_service)):
    # 입력 DTO → Service → DB. 성공 시 201, 응답은 RouteOut(Pydantic)
    route = routes_service.create_route(route_create)
    return CommonResponse(code=201, message="경로 생성 성공", data=route)

# 수정
@router.patch(
    "",
    response_model=CommonResponse[RouteOut],
    status_code=status.HTTP_200_OK,
)
def update(route_update: RouteUpdate, routes_service: RoutesService = Depends(get_routes_service)):
    # 부분 수정. 유효성/제약 위반은 Service에서 처리.
    route = routes_service.update_route(route_update)
    return CommonResponse(code=200, message="경로 수정 성공", data=route)

# 삭제
@router.delete(
    "/{route_id}",
    response_model=CommonResponse[RouteOut],
    status_code=status.HTTP_200_OK,
)
def delete(route_id: int, routes_service: RoutesService = Depends(get_routes_service)):
    # id로 삭제. 없으면 ControlledException으로 터뜨림 → 전역 핸들러에서 공통 처리.
    route = routes_service.delete_route_by_id(route_id)
    return CommonResponse(code=200, message="경로 삭제 성공", data=route)

# 전체 조회
@router.get(
    "",
    response_model=CommonResponse[list[RouteOut]],
    status_code=status.HTTP_200_OK,
)
def get_all(routes_service: RoutesService = Depends(get_routes_service)):
    # 리스트 반환. Service는 단순 위임.
    routes = routes_service.find_all()
    return CommonResponse(code=200, message="경로 전체 조회 성공", data=routes)

# 개별 조회
@router.get(
    "/{route_id}",
    response_model=CommonResponse[RouteOut],
    status_code=status.HTTP_200_OK,
)
def read_by_id(route_id: int, routes_service: RoutesService = Depends(get_routes_service)):
    # 동적 파라미터는 맨 마지막. 경로 충돌 방지.
    route = routes_service.find_by_id(route_id)
    return CommonResponse(code=200, message="경로 조회 성공", data=route)
