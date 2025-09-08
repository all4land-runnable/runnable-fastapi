# app/routers/user_paces/user_paces_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.routers.user_paces.user_paces import UserPaces

class UserPacesRepository:
    def __init__(self, database: Session) -> None:
        # Repository는 DB 접근 전용. 트랜잭션(Commit/Rollback) 모름.
        self.database = database

    # 트랜잭션은 Service가 관리 → 여기선 commit() 하지 않음
    def save(self, user_pace: UserPaces) -> UserPaces:
        # add로 pending에 올리고, flush로 즉시 INSERT 실행 + PK 확보.
        self.database.add(user_pace)
        self.database.flush()   # PK 확보/조기 예외 감지
        return user_pace

    def find_by_id(self, user_pace_id: int) -> Optional[UserPaces]:
        # PK 조회 최단코스. 없으면 None.
        return self.database.get(UserPaces, user_pace_id)

    def find_all(self) -> List[UserPaces]:
        # 전체 조회. scalars()로 엔티티 컬럼만 뽑고, all() → list 캐스팅.
        return list(self.database.execute(select(UserPaces)).scalars().all())

    def find_by_user_strategy_id(self, user_strategy_id: int) -> List[UserPaces]:
        stmt = select(UserPaces).where(UserPaces.user_strategy_id == user_strategy_id)
        return list(self.database.execute(stmt).scalars().all())

    def find_by_section_id(self, section_id: int) -> List[UserPaces]:
        stmt = select(UserPaces).where(UserPaces.section_id == section_id)
        return list(self.database.execute(stmt).scalars().all())

    def delete(self, user_pace: UserPaces) -> None:
        # 삭제는 Service에서 commit으로 마무리.
        self.database.delete(user_pace)

    def delete_by_id(self, user_pace_id: int) -> bool:
        # 편의용. True면 삭제 예정 상태, 커밋은 Service에서.
        up = self.find_by_id(user_pace_id)
        if not up:
            return False
        self.database.delete(up)
        return True
