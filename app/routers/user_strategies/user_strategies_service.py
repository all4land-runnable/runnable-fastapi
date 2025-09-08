# app/routers/user_strategies/user_strategies_service.py
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.internal.exception.controlled_exception import ControlledException
from app.internal.exception.errorcode import user_strategies_error_code
from app.routers.user_strategies.user_strategies import UserStrategies
from app.routers.user_strategies.user_strategies_dto import UserStrategyCreate, UserStrategyUpdate
from app.routers.user_strategies.user_strategies_repository import UserStrategiesRepository

class UserStrategiesService:
    def __init__(self, database: Session, user_strategies_repository: UserStrategiesRepository) -> None:
        # Service는 트랜잭션 경계(Commit/Rollback) + 의미있는 예외 매핑 담당.
        self.database = database
        self.user_strategies_repository = user_strategies_repository

    # 생성
    def create_user_strategy(self, dto: UserStrategyCreate) -> UserStrategies:
        us = UserStrategies(
            user_route_id=dto.user_route_id,
            luggage_weight=dto.luggage_weight,
            pace_average=dto.pace_average,
        )
        try:
            self.user_strategies_repository.save(us) # flush까지 하고 PK 확보
            self.database.commit()                   # [핵심] 트랜잭션 확정은 Service에서만
        except IntegrityError as e:
            self.database.rollback()
            # 유니크 위반 매핑
            raise ControlledException(user_strategies_error_code.DUPLICATE_KEY) from e

        self.database.refresh(us)                   # server_default/trigger 동기화
        return us

    # 조회 (없으면 예외)
    def find_by_id(self, user_strategy_id: int) -> UserStrategies:
        us = self.user_strategies_repository.find_by_id(user_strategy_id)
        if not us:
            raise ControlledException(user_strategies_error_code.USER_STRATEGY_NOT_FOUND)
        return us

    def find_all(self) -> List[UserStrategies]:
        items = self.user_strategies_repository.find_all()
        if not items:
            raise ControlledException(user_strategies_error_code.USER_STRATEGY_NOT_FOUND)
        return items

    # 갱신
    def update_user_strategy(self, dto: UserStrategyUpdate) -> UserStrategies:
        us = self.user_strategies_repository.find_by_id(dto.user_strategy_id)
        if not us:
            raise ControlledException(user_strategies_error_code.USER_STRATEGY_NOT_FOUND)

        # [명준 주석]
        # - 화이트리스트 필드만 반영. 실수로 다른 속성 들어오는 것 차단.
        allowed = {"user_route_id", "luggage_weight", "pace_average", "is_deleted"}
        data = dto.model_dump(exclude_none=True)  # None 값들은 아예 제외
        for k, v in data.items():
            if k in allowed and k != "user_strategy_id":
                setattr(us, k, v)

        try:
            self.database.commit()
        except IntegrityError as e:
            self.database.rollback()
            # 갱신 중 유니크 위반도 동일하게 매핑
            raise ControlledException(user_strategies_error_code.DUPLICATE_KEY) from e
        self.database.refresh(us)
        return us

    # 삭제
    def delete_user_strategy_by_id(self, user_strategy_id: int) -> UserStrategies:
        us = self.user_strategies_repository.find_by_id(user_strategy_id)
        if not us:
            raise ControlledException(user_strategies_error_code.USER_STRATEGY_NOT_FOUND)
        self.user_strategies_repository.delete(us)
        self.database.commit()  # delete는 커밋까지 해야 반영
        return us
