from fastapi import APIRouter, Depends
from starlette import status

from sqlalchemy.orm import Session

from app.routers.users import users_service
from app.routers.users.users_dto import UserCreate, UserUpdate, UserDelete, UserOut
from config.common.common_response import CommonResponse
from config.database.postgres_database import get_database

router = APIRouter(prefix="/users", tags=["users"])

# 생성 ------------------------------------------------------------
@router.post(
    "",
    response_model=CommonResponse[UserOut],
    status_code=status.HTTP_201_CREATED,
)
def create_user(user_create: UserCreate, db: Session = Depends(get_database)):
    user = users_service.create_user(db, user_create)
    return CommonResponse(code=201, message="유저 생성 성공", data=user)

# 수정 ------------------------------------------------------------
@router.patch(
    "",
    response_model=CommonResponse[UserOut],
    status_code=status.HTTP_200_OK,
)
def update(user_update: UserUpdate, db: Session = Depends(get_database)):
    user = users_service.update_user_by_id(
        db,
        user_update.id,
        email=user_update.email,
        username=user_update.username,
        password=user_update.password,
        is_active=user_update.is_active,
    )
    return CommonResponse(code=200, message="유저 수정 성공", data=user)

# 삭제 ------------------------------------------------------------
@router.delete(
    "",
    response_model=CommonResponse[UserOut],
    status_code=status.HTTP_200_OK,
)
def delete(user_delete: UserDelete, db: Session = Depends(get_database)):
    user = users_service.delete_user_by_id(db, user_delete.id)
    return CommonResponse(code=200, message="유저 삭제 성공", data=user)

# 전체 조회 --------------------------------------------------------
@router.get(
    "",
    response_model=CommonResponse[list[UserOut]],
    status_code=status.HTTP_200_OK,
)
def get_all(db: Session = Depends(get_database)):
    users = users_service.find_all(db)
    return CommonResponse(code=200, message="유저 전체 조회 성공", data=users)

# 개별 조회들 (정적 경로 → 동적 경로 순서 유지) ------------------------
@router.get(
    "/email/{email}",
    response_model=CommonResponse[UserOut],
    status_code=status.HTTP_200_OK,
)
def read_by_email(email: str, db: Session = Depends(get_database)):
    user = users_service.find_by_email(db, email)  # Optional 반환 → service에서 not found 예외 변환
    return CommonResponse(code=200, message="유저 조회 성공", data=user)

@router.get(
    "/username/{username}",
    response_model=CommonResponse[UserOut],
    status_code=status.HTTP_200_OK,
)
def read_by_username(username: str, db: Session = Depends(get_database)):
    user = users_service.find_by_username(db, username)
    return CommonResponse(code=200, message="유저 조회 성공", data=user)

@router.get(
    "/{id}",
    response_model=CommonResponse[UserOut],
    status_code=status.HTTP_200_OK,
)
def read_by_id(id: int, db: Session = Depends(get_database)):
    user = users_service.find_by_id(db, id)
    return CommonResponse(code=200, message="유저 조회 성공", data=user)
