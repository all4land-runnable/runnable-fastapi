# app/services/users_service.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.internal.exception.controlled_exception import ControlledException
from app.internal.exception.errorcode import user_error_code
from app.routers.users.users import Users
from app.routers.users.users_dto import UserCreate
from app.routers.users.users_repository import UsersRepository, SqlAlchemyUsersRepository


# 생성
def create_user(database: Session, payload: UserCreate, repo: UsersRepository | None = None) -> Users:
    repo = repo or SqlAlchemyUsersRepository(database)
    user = Users(
        email=payload.email,
        username=payload.username,
        password=payload.password,  # TODO: 해시로 변경
    )
    repo.save_new(user)
    try:
        database.commit()
    except IntegrityError as e:
        database.rollback()
        raise ControlledException(user_error_code.DUPLICATE_KEY) from e
    database.refresh(user)
    return user

# 조회 (Optional 반환: JPA Optional 느낌)
def find_by_id(database: Session, user_id: int,
               repo: UsersRepository | None = None) -> Optional[Users]:
    repo = repo or SqlAlchemyUsersRepository(database)
    return repo.find_by_id(user_id)

def find_by_email(database: Session, email: str,
                  repo: UsersRepository | None = None) -> Optional[Users]:
    repo = repo or SqlAlchemyUsersRepository(database)
    return repo.find_by_email(email)

def find_by_username(database: Session, username: str,
                     repo: UsersRepository | None = None) -> Optional[Users]:
    repo = repo or SqlAlchemyUsersRepository(database)
    return repo.find_by_username(username)

def find_all(database: Session,
             repo: UsersRepository | None = None) -> List[Users]:
    repo = repo or SqlAlchemyUsersRepository(database)
    return repo.find_all()

# 갱신 (Service에서 존재확인 + 트랜잭션/예외 매핑)
def update_user_by_id(database: Session, user_id: int, **fields) -> Users:
    repo = SqlAlchemyUsersRepository(database)
    user = repo.find_by_id(user_id)
    if not user:
        raise ControlledException(user_error_code.USER_NOT_FOUND)

    allowed = {"email", "username", "password", "is_active"}  # password는 해시 저장
    for k, v in fields.items():
        if k in allowed and v is not None:
            setattr(user, k, v)

    try:
        database.commit()
    except IntegrityError as e:
        database.rollback()
        raise ControlledException(user_error_code.DUPLICATE_KEY) from e
    database.refresh(user)
    return user

# 삭제 (Service에서 존재확인/예외 변환)
def delete_user_by_id(database: Session, user_id: int) -> Users:
    repo = SqlAlchemyUsersRepository(database)
    user = repo.find_by_id(user_id)
    if not user:
        raise ControlledException(user_error_code.USER_NOT_FOUND)

    repo.delete(user)
    database.commit()
    return user
