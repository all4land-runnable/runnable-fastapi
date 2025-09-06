# app/routers/users/users_controller.py
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from app.routers.users.users_dto import UserCreate, UserUpdate, UserDelete, UserOut
from app.routers.users.users_repository import UsersRepository
from app.routers.users.users_service import UsersService
from config.common.common_response import CommonResponse
from config.database.postgres_database import get_database  # Session 제공

router = APIRouter(prefix="/users", tags=["users"])

# - 여기서 Service 인스턴스를 DI로 주입한다.
# - 포인트: 라우터는 비즈니스 로직 모름. 의존성으로 Service만 받아서 호출.
# - Session은 요청 단위로 열고 닫힘(get_database). 메모리 누수 방지.
def get_users_service(database: Session = Depends(get_database)) -> UsersService:
    users_repository = UsersRepository(database)           # Repository는 트랜잭션 모름(Commit 금지)
    return UsersService(database, users_repository)        # Service가 트랜잭션/예외 관리 담당

# 생성
@router.post(
    "",
    response_model=CommonResponse[UserOut],
    status_code=status.HTTP_201_CREATED,
)
def create_user(user_create: UserCreate, users_service: UsersService = Depends(get_users_service)):
    # 입력 DTO → Service → DB. 성공 시 201, 응답은 UserOut(Pydantic)으로 민감정보 방지.
    user = users_service.create_user(user_create)
    return CommonResponse(code=201, message="유저 생성 성공", data=user)

# 수정
@router.patch(
    "",
    response_model=CommonResponse[UserOut],
    status_code=status.HTTP_200_OK,
)
def update(user_update: UserUpdate, users_service: UsersService = Depends(get_users_service)):
    # 부분 수정. 유효성/중복 키는 Service에서 처리.
    user = users_service.update_user(user_update)
    return CommonResponse(code=200, message="유저 수정 성공", data=user)

# 삭제
@router.delete(
    "",
    response_model=CommonResponse[UserOut],
    status_code=status.HTTP_200_OK,
)
def delete(user_delete: UserDelete, users_service: UsersService = Depends(get_users_service)):
    # id로 삭제. 없으면 ControlledException으로 터뜨림 → 전역 핸들러에서 공통 처리.
    user = users_service.delete_user_by_id(user_delete.id)
    return CommonResponse(code=200, message="유저 삭제 성공", data=user)

# 전체 조회
@router.get(
    "",
    response_model=CommonResponse[list[UserOut]],
    status_code=status.HTTP_200_OK,
)
def get_all(users_service: UsersService = Depends(get_users_service)):
    # 리스트 반환. Service는 단순 위임.
    users = users_service.find_all()
    return CommonResponse(code=200, message="유저 전체 조회 성공", data=users)

# 개별 조회들 (정적 → 동적 순서)
@router.get(
    "/email/{email}",
    response_model=CommonResponse[UserOut],
    status_code=status.HTTP_200_OK,
)
def read_by_email(email: str, users_service: UsersService = Depends(get_users_service)):
    # 유니크 한정. 없으면 Service에서 예외.
    user = users_service.find_by_email(email)  # 내부에서 not found → ControlledException
    return CommonResponse(code=200, message="유저 조회 성공", data=user)

@router.get(
    "/username/{username}",
    response_model=CommonResponse[UserOut],
    status_code=status.HTTP_200_OK,
)
def read_by_username(username: str, users_service: UsersService = Depends(get_users_service)):
    # username 유니크 가정. 없으면 예외.
    user = users_service.find_by_username(username)
    return CommonResponse(code=200, message="유저 조회 성공", data=user)

@router.get(
    "/{id}",
    response_model=CommonResponse[UserOut],
    status_code=status.HTTP_200_OK,
)
def read_by_id(id: int, users_service: UsersService = Depends(get_users_service)):
    # 동적 파라미터는 맨 마지막. 경로 충돌 방지.
    user = users_service.find_by_id(id)
    return CommonResponse(code=200, message="유저 조회 성공", data=user)
