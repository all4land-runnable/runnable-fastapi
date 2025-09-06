from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from app.routers.users import users_service
from app.routers.users.users import Users
from app.routers.users.users_dto import UsersDTO
from config.common.common_response import CommonResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "",
    response_model=CommonResponse[Users],
    status_code=status.HTTP_200_OK,
)
async def create_user(users_dto: UsersDTO, response: Response):
    user = users_service.create(users_dto)

    return CommonResponse(code=200, message="유저 생성 성공", data=user)

@router.patch(
    "",
    response_model=CommonResponse[Users],
    status_code=status.HTTP_200_OK
)
async def update(users_dto: UsersDTO, response: Response):
    user = users_service.update(users_dto)
    return CommonResponse(code=200, message="유저 수정 성공", data=user)

@router.delete(
    "",
    response_model=CommonResponse[Users],
    status_code=status.HTTP_200_OK
)
async def delete(users_dto: UsersDTO, response: Response):
    user = users_service.delete(users_dto)
    return CommonResponse(code=200, message="유저 삭제 성공", data=user)

@router.get(
    "",
    response_model=CommonResponse[list[Users]],
    status_code=status.HTTP_200_OK
)
async def get_all(response: Response):
    users = users_service.find_all()
    return CommonResponse(code=200, message="유저 전체 조회 성공", data=users)

@router.get(
    "/{id}",
    response_model=CommonResponse[Users],
    status_code=status.HTTP_200_OK
)
async def read_by_id(id: int, response: Response):
    user = users_service.find_by_id(id)
    return CommonResponse(
        code=200,
        message="유저 조회 성공",
        data=user
    )

@router.get(
    "/email/{email}",
    response_model=CommonResponse[Users],
    status_code=status.HTTP_200_OK
)
async def read_by_email(email: str, response: Response):
    user = users_service.find_by_email(email)
    return CommonResponse(
        code=200,
        message="유저 조회 성공",
        data=user
    )

@router.get(
    "/username/{username}",
    response_model=CommonResponse[Users],
    status_code=status.HTTP_200_OK
)
async def read_by_username(username: str, response: Response):
    user = users_service.find_by_username(username)
    return CommonResponse(
        code=200,
        message="유저 조회 성공",
        data=user
    )