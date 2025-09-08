# app/routers/user_strategies/user_strategies_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.routers.user_strategies.user_strategies import UserStrategies

class UserStrategiesRepository:
    def __init__(self, database: Session) -> None:
        # Repository는 DB 접근 전용. 트랜잭션(Commit/Rollback) 모름.
        self.database = database

    # 트랜잭션은 Service가 관리 → 여기선 commit() 하지 않음
    def save(self, user_strategy: UserStrategies) -> UserStrategies:
        # add로 pending에 올리고, flush로 즉시 INSERT 실행 + PK 확보.
        self.database.add(user_strategy)
        self.database.flush()   # PK 확보/조기 예외 감지
        return user_strategy

    def find_by_id(self, user_strategy_id: int) -> Optional[UserStrategies]:
        # PK 조회 최단코스. 없으면 None.
        return self.database.get(UserStrategies, user_strategy_id)

    def find_by_user_route_id(self, user_route_id: int) -> Optional[UserStrategies]:
        # 한 user_route 당 0/1건
        return self.database.execute(
            select(UserStrategies).where(UserStrategies.user_route_id == user_route_id)
        ).scalar_one_or_none()

    def find_all(self) -> List[UserStrategies]:
        # 전체 조회. scalars()로 엔티티 컬럼만 뽑고, all() → list 캐스팅.
        return list(self.database.execute(select(UserStrategies)).scalars().all())

    def delete(self, user_strategy: UserStrategies) -> None:
        # 삭제는 Service에서 commit으로 마무리.
        self.database.delete(user_strategy)

    def delete_by_id(self, user_strategy_id: int) -> bool:
        # 편의용. True면 삭제 예정 상태, 커밋은 Service에서.
        us = self.find_by_id(user_strategy_id)
        if not us:
            return False
        self.database.delete(us)
        return True
