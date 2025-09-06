# app/repositories/users_repository.py
from typing import Protocol, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.routers.users.users import Users

class UsersRepository(Protocol):
    def save_new(self, user: Users) -> Users: ...
    def update(self, user: Users) -> Users: ...
    def find_by_id(self, user_id: int) -> Optional[Users]: ...
    def find_by_email(self, email: str) -> Optional[Users]: ...
    def find_by_username(self, username: str) -> Optional[Users]: ...
    def find_all(self) -> List[Users]: ...
    def delete(self, user: Users) -> None: ...
    def delete_by_id(self, user_id: int) -> bool: ...

class SqlAlchemyUsersRepository(UsersRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    # 트랜잭션은 Service가 관리 → 여기선 commit() 하지 않음
    def save_new(self, user: Users) -> Users:
        self.db.add(user)
        self.db.flush()          # PK 미리 확보가 필요할 수 있어 flush
        return user

    def update(self, user: Users) -> Users:
        # 변경감지(autoflush) 기반이라 별도 작업 불필요
        self.db.flush()
        return user

    def find_by_id(self, user_id: int) -> Optional[Users]:
        return self.db.get(Users, user_id)

    def find_by_email(self, email: str) -> Optional[Users]:
        return self.db.execute(
            select(Users).where(Users.email == email)
        ).scalar_one_or_none()

    def find_by_username(self, username: str) -> Optional[Users]:
        return self.db.execute(
            select(Users).where(Users.username == username)
        ).scalar_one_or_none()

    def find_all(self) -> List[Users]:
        return list(self.db.execute(select(Users)).scalars().all())

    def delete(self, user: Users) -> None:
        self.db.delete(user)

    def delete_by_id(self, user_id: int) -> bool:
        user = self.find_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        return True
