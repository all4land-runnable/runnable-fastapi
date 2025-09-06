from typing import List

from app.internal.exception.controlled_exception import ControlledException
from app.internal.exception.errorcode import basic_error_code
from app.internal.utils.optional_helper import or_else_throw
from app.routers.users import users_repository
from app.routers.users.users import Users
from app.routers.users.users_dto import UsersDTO


def create(users_dto: UsersDTO) -> Users:
    newUser = Users(
        id=users_dto.id,
        email=users_dto.email,
        password=users_dto.password,
        username=users_dto.username,
        created_at=users_dto.created_at,
        updated_at=users_dto.updated_at
    )

    return users_repository.insert_into(newUser)

def update(users_dto: UsersDTO) -> Users:
    user = or_else_throw(
        value=users_repository.find_by_id(users_dto.id),
        error=ControlledException(basic_error_code.DATABASE_ERROR)
    )

    if users_dto.email is not None:
        user.email = users_dto.email
    if users_dto.password is not None:
        user.password = users_dto.password
    if users_dto.username is not None:
        user.username = users_dto.username

    return users_repository.update_into(user)

def delete(users_dto: UsersDTO) -> Users:
    user = or_else_throw(
        value=users_repository.find_by_id(users_dto.id),
        error=ControlledException(basic_error_code.DATABASE_ERROR)
    )

    return users_repository.delete_users(user)

def find_by_id(user_id: int) -> Users:
    return or_else_throw(
        value=users_repository.find_by_id(user_id),
        error=ControlledException(basic_error_code.DATABASE_ERROR)
    )

def find_by_email(email: str) -> Users:
    return or_else_throw(
        value=users_repository.find_by_email(email),
        error=ControlledException(basic_error_code.DATABASE_ERROR)
    )

def find_by_username(username: str) -> Users:
    return or_else_throw(
        value=users_repository.find_by_username(username),
        error=ControlledException(basic_error_code.DATABASE_ERROR)
    )

def find_all() -> List[Users]:
    return users_repository.find_all()