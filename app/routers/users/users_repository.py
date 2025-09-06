# app/routers/users/users_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.routers.users.users import Users

class UsersRepository:
    def __init__(self, database: Session) -> None:
        # Repository는 DB 접근 전용. 트랜잭션(Commit/Rollback) 모름.
        self.database = database

    # 트랜잭션은 Service가 관리 → 여기선 commit() 하지 않음
    def save(self, user: Users) -> Users:
        # add로 pending에 올리고, flush로 즉시 INSERT 실행 + PK 확보.
        self.database.add(user)
        self.database.flush()   # PK 확보/조기 예외 감지
        return user

    def find_by_id(self, user_id: int) -> Optional[Users]:
        # PK 조회 최단코스. 없으면 None.
        return self.database.get(Users, user_id)

    def find_by_email(self, email: str) -> Optional[Users]:
        # 유니크 조건 가정. 0/1 건만 나와야 함.
        return self.database.execute(
            select(Users).where(Users.email == email)
        ).scalar_one_or_none()

    def find_by_username(self, username: str) -> Optional[Users]:
        # 마찬가지로 유니크 가정.
        return self.database.execute(
            select(Users).where(Users.username == username)
        ).scalar_one_or_none()

    def find_all(self) -> List[Users]:
        # 전체 조회. scalars()로 엔티티 컬럼만 뽑고, all() → list 캐스팅.
        return list(self.database.execute(select(Users)).scalars().all())

    def delete(self, user: Users) -> None:
        # 삭제는 Service에서 commit으로 마무리.
        self.database.delete(user)

    def delete_by_id(self, user_id: int) -> bool:
        # 편의용. True면 삭제 예정 상태, 커밋은 Service에서.
        user = self.find_by_id(user_id)
        if not user:
            return False
        self.database.delete(user)
        return True
