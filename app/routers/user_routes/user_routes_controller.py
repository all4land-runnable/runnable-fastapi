# app/routers/user_routes/user_routes_controller.py
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from app.routers.user_routes.user_routes_dto import UserRouteCreate, UserRouteUpdate, UserRouteOut
from app.routers.user_routes.user_routes_repository import UserRoutesRepository
from app.routers.user_routes.user_routes_service import UserRoutesService
from config.common.common_response import CommonResponse
from config.database.postgres_database import get_database  # Session 제공

router = APIRouter(prefix="/user-routes", tags=["user_routes"])

# - 여기서 Service 인스턴스를 DI로 주입한다.
# - 포인트: 라우터는 비즈니스 로직 모름. 의존성으로 Service만 받아서 호출.
# - Session은 요청 단위로 열고 닫힘(get_database). 메모리 누수 방지.
def get_user_routes_service(database: Session = Depends(get_database)) -> UserRoutesService:
    repo = UserRoutesRepository(database)                   # Repository는 트랜잭션 모름(Commit 금지)
    return UserRoutesService(database, repo)                # Service가 트랜잭션/예외 관리 담당

# 생성
@router.post(
    "",
    response_model=CommonResponse[UserRouteOut],
    status_code=status.HTTP_201_CREATED,
)
def create_user_route(dto: UserRouteCreate, service: UserRoutesService = Depends(get_user_routes_service)):
    # 입력 DTO → Service → DB. 성공 시 201, 응답은 UserRouteOut(Pydantic)
    ur = service.create_user_route(dto)
    return CommonResponse(code=201, message="유저-루트 매핑 생성 성공", data=ur)

# 수정
@router.patch(
    "",
    response_model=CommonResponse[UserRouteOut],
    status_code=status.HTTP_200_OK,
)
def update(dto: UserRouteUpdate, service: UserRoutesService = Depends(get_user_routes_service)):
    # 부분 수정. 유효성/중복 키는 Service에서 처리.
    ur = service.update_user_route(dto)
    return CommonResponse(code=200, message="유저-루트 매핑 수정 성공", data=ur)

# 삭제
@router.delete(
    "/{user_route_id}",
    response_model=CommonResponse[UserRouteOut],
    status_code=status.HTTP_200_OK,
)
def delete(user_route_id: int, service: UserRoutesService = Depends(get_user_routes_service)):
    # id로 삭제. 없으면 ControlledException으로 터뜨림 → 전역 핸들러에서 공통 처리.
    ur = service.delete_user_route_by_id(user_route_id)
    return CommonResponse(code=200, message="유저-루트 매핑 삭제 성공", data=ur)

# 전체 조회
@router.get(
    "",
    response_model=CommonResponse[list[UserRouteOut]],
    status_code=status.HTTP_200_OK,
)
def get_all(service: UserRoutesService = Depends(get_user_routes_service)):
    # 리스트 반환. Service는 단순 위임.
    urs = service.find_all()
    return CommonResponse(code=200, message="유저-루트 매핑 전체 조회 성공", data=urs)

# 개별 조회
@router.get(
    "/{user_route_id}",
    response_model=CommonResponse[UserRouteOut],
    status_code=status.HTTP_200_OK,
)
def read_by_id(user_route_id: int, service: UserRoutesService = Depends(get_user_routes_service)):
    # 동적 파라미터는 맨 마지막. 경로 충돌 방지.
    ur = service.find_by_id(user_route_id)
    return CommonResponse(code=200, message="유저-루트 매핑 조회 성공", data=ur)
