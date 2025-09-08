from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.internal.exception.controlled_exception import ControlledException
from app.internal.exception.errorcode import user_error_code
from app.routers.users.users import Users
from app.routers.users.users_dto import UserCreate, UserUpdate
from app.routers.users.users_repository import UsersRepository

class UsersService:
    def __init__(self, database: Session, users_repository: UsersRepository) -> None:
        # Service는 트랜잭션 경계(Commit/Rollback) + 의미있는 예외 매핑 담당.
        self.database = database
        self.users_repository = users_repository

    # 생성
    def create_user(self, user_create: UserCreate) -> Users:
        # 절대 평문 저장 금지. TODO에 해시 처리 추가 예정.
        user = Users(
            email=user_create.email,
            username=user_create.username,
            password=user_create.password, # TODO: 해시로 변경
            age=user_create.age,
            runner_since=user_create.runner_since,
            pace_average=user_create.pace_average,
        )
        try:
            self.users_repository.save(user) # flush까지 하고 PK 확보
            self.database.commit() # [핵심] 트랜잭션 확정은 Service에서만
        except IntegrityError as e:
            self.database.rollback()
            # 중복 키(유니크 위반) 비즈니스 에러코드로 변환
            raise ControlledException(user_error_code.DUPLICATE_KEY) from e

        self.database.refresh(user) # server_default/trigger 동기화
        return user

    # 조회 (없으면 예외)
    def find_by_id(self, user_id: int) -> Users:
        # Optional 존재 보장으로 승격(없으면 예외)
        user = self.users_repository.find_by_id(user_id)
        if not user:
            raise ControlledException(user_error_code.USER_NOT_FOUND)
        return user

    def find_by_email(self, email: str) -> Users:
        user = self.users_repository.find_by_email(email)
        if not user:
            raise ControlledException(user_error_code.USER_NOT_FOUND)
        return user

    def find_by_username(self, username: str) -> Users:
        user = self.users_repository.find_by_username(username)
        if not user:
            raise ControlledException(user_error_code.USER_NOT_FOUND)
        return user

    def find_all(self)-> List[Users]:
        users = self.users_repository.find_all()
        if not users:
            raise ControlledException(user_error_code.USER_NOT_FOUND)
        return users

    # 갱신
    def update_user(self, user_update: UserUpdate) -> Users:
        # 존재 확인부터. 여기서 못 찾으면 아래 로직 전부 스킵.
        user = self.users_repository.find_by_id(user_update.user_id) # ← id → user_id

        if not user:
            raise ControlledException(user_error_code.USER_NOT_FOUND)

        # [명준 주석]
        # - 화이트리스트 필드만 반영. 실수로 다른 속성 들어오는 것 차단.
        allowed = {"email", "username", "password", "is_deleted", "age", "runner_since", "pace_average"}
        data = user_update.model_dump(exclude_none=True) # None 값들은 아예 제외
        for k, v in data.items():
            if k in allowed and k != "user_id":
                setattr(user, k, v)

        try:
            self.database.commit()
        except IntegrityError as e:
            self.database.rollback()
            # 갱신 중 중복 키도 동일하게 매핑
            raise ControlledException(user_error_code.DUPLICATE_KEY) from e
        self.database.refresh(user)
        return user

    # 삭제
    def delete_user_by_id(self, user_id: int) -> Users:
        # 먼저 존재 확인 → 없으면 도메인 예외
        user = self.users_repository.find_by_id(user_id)
        if not user:
            raise ControlledException(user_error_code.USER_NOT_FOUND)
        self.users_repository.delete(user)
        self.database.commit() # delete는 커밋까지 해야 반영
        return user
