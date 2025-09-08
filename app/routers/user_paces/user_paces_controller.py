# app/routers/user_paces/user_paces_controller.py
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from app.routers.user_paces.user_paces_dto import UserPaceCreate, UserPaceUpdate, UserPaceOut
from app.routers.user_paces.user_paces_repository import UserPacesRepository
from app.routers.user_paces.user_paces_service import UserPacesService
from config.common.common_response import CommonResponse
from config.database.postgres_database import get_database  # Session 제공

router = APIRouter(prefix="/user-paces", tags=["user_paces"])

# - 여기서 Service 인스턴스를 DI로 주입한다.
# - 포인트: 라우터는 비즈니스 로직 모름. 의존성으로 Service만 받아서 호출.
# - Session은 요청 단위로 열고 닫힘(get_database). 메모리 누수 방지.
def get_user_paces_service(database: Session = Depends(get_database)) -> UserPacesService:
    repo = UserPacesRepository(database)                     # Repository는 트랜잭션 모름(Commit 금지)
    return UserPacesService(database, repo)                  # Service가 트랜잭션/예외 관리 담당

# 생성
@router.post(
    "",
    response_model=CommonResponse[UserPaceOut],
    status_code=status.HTTP_201_CREATED,
)
def create_user_pace(dto: UserPaceCreate, svc: UserPacesService = Depends(get_user_paces_service)):
    up = svc.create_user_pace(dto)
    return CommonResponse(code=201, message="유저 페이스 생성 성공", data=up)

# 수정
@router.patch(
    "",
    response_model=CommonResponse[UserPaceOut],
    status_code=status.HTTP_200_OK,
)
def update_user_pace(dto: UserPaceUpdate, svc: UserPacesService = Depends(get_user_paces_service)):
    up = svc.update_user_pace(dto)
    return CommonResponse(code=200, message="유저 페이스 수정 성공", data=up)

# 삭제
@router.delete(
    "/{user_pace_id}",
    response_model=CommonResponse[UserPaceOut],
    status_code=status.HTTP_200_OK,
)
def delete_user_pace(user_pace_id: int, svc: UserPacesService = Depends(get_user_paces_service)):
    up = svc.delete_user_pace_by_id(user_pace_id)
    return CommonResponse(code=200, message="유저 페이스 삭제 성공", data=up)

# 전체 조회
@router.get(
    "",
    response_model=CommonResponse[list[UserPaceOut]],
    status_code=status.HTTP_200_OK,
)
def get_all(svc: UserPacesService = Depends(get_user_paces_service)):
    ups = svc.find_all()
    return CommonResponse(code=200, message="유저 페이스 전체 조회 성공", data=ups)

# user_strategy_id로 조회
@router.get(
    "/strategy/{user_strategy_id}",
    response_model=CommonResponse[list[UserPaceOut]],
    status_code=status.HTTP_200_OK,
)
def read_by_strategy(user_strategy_id: int, svc: UserPacesService = Depends(get_user_paces_service)):
    ups = svc.find_by_user_strategy_id(user_strategy_id)
    return CommonResponse(code=200, message="유저 페이스 조회 성공", data=ups)

# section_id로 조회
@router.get(
    "/section/{section_id}",
    response_model=CommonResponse[list[UserPaceOut]],
    status_code=status.HTTP_200_OK,
)
def read_by_section(section_id: int, svc: UserPacesService = Depends(get_user_paces_service)):
    ups = svc.find_by_section_id(section_id)
    return CommonResponse(code=200, message="유저 페이스 조회 성공", data=ups)

# 개별 조회
@router.get(
    "/{user_pace_id}",
    response_model=CommonResponse[UserPaceOut],
    status_code=status.HTTP_200_OK,
)
def read_by_id(user_pace_id: int, svc: UserPacesService = Depends(get_user_paces_service)):
    up = svc.find_by_id(user_pace_id)
    return CommonResponse(code=200, message="유저 페이스 조회 성공", data=up)
