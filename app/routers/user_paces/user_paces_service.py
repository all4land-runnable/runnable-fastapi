# app/routers/user_paces/user_paces_service.py
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.internal.exception.controlled_exception import ControlledException
from app.internal.exception.errorcode import user_paces_error_code
from app.routers.user_paces.user_paces import UserPaces
from app.routers.user_paces.user_paces_dto import UserPaceCreate, UserPaceUpdate
from app.routers.user_paces.user_paces_repository import UserPacesRepository

class UserPacesService:
    def __init__(self, database: Session, user_paces_repository: UserPacesRepository) -> None:
        # Service는 트랜잭션 경계(Commit/Rollback) + 의미있는 예외 매핑 담당.
        self.database = database
        self.user_paces_repository = user_paces_repository

    # 생성
    def create_user_pace(self, dto: UserPaceCreate) -> UserPaces:
        up = UserPaces(
            user_strategy_id=dto.user_strategy_id,
            section_id=dto.section_id,
            pace=dto.pace,
            strategy=dto.strategy,
            foundation_latitude=dto.foundation_latitude,
            foundation_longitude=dto.foundation_longitude,
        )
        try:
            self.user_paces_repository.save(up)  # flush까지 하고 PK 확보
            self.database.commit()               # [핵심] 트랜잭션 확정은 Service에서만
        except IntegrityError as e:
            self.database.rollback()
            # FK/유니크 위반 등 → 비즈니스 에러코드로 변환
            raise ControlledException(user_paces_error_code.DUPLICATE_KEY) from e

        self.database.refresh(up)                # server_default/trigger 동기화
        return up

    # 조회 (없으면 예외)
    def find_by_id(self, user_pace_id: int) -> UserPaces:
        up = self.user_paces_repository.find_by_id(user_pace_id)
        if not up:
            raise ControlledException(user_paces_error_code.USER_PACE_NOT_FOUND)
        return up

    def find_all(self) -> List[UserPaces]:
        lst = self.user_paces_repository.find_all()
        if not lst:
            # 빈 리스트를 허용하고 싶다면 이 예외를 제거하세요.
            raise ControlledException(user_paces_error_code.USER_PACE_NOT_FOUND)
        return lst

    def find_by_user_strategy_id(self, user_strategy_id: int) -> List[UserPaces]:
        lst = self.user_paces_repository.find_by_user_strategy_id(user_strategy_id)
        if not lst:
            raise ControlledException(user_paces_error_code.USER_PACE_NOT_FOUND)
        return lst

    def find_by_section_id(self, section_id: int) -> List[UserPaces]:
        lst = self.user_paces_repository.find_by_section_id(section_id)
        if not lst:
            raise ControlledException(user_paces_error_code.USER_PACE_NOT_FOUND)
        return lst

    # 갱신
    def update_user_pace(self, dto: UserPaceUpdate) -> UserPaces:
        up = self.user_paces_repository.find_by_id(dto.user_pace_id)
        if not up:
            raise ControlledException(user_paces_error_code.USER_PACE_NOT_FOUND)

        # 화이트리스트 필드만 반영
        allowed = {
            "user_strategy_id", "section_id",
            "pace", "strategy", "foundation_latitude", "foundation_longitude",
        }
        data = dto.model_dump(exclude_none=True)
        for k, v in data.items():
            if k in allowed and k != "user_pace_id":
                setattr(up, k, v)

        try:
            self.database.commit()
        except IntegrityError as e:
            self.database.rollback()
            raise ControlledException(user_paces_error_code.DUPLICATE_KEY) from e
        self.database.refresh(up)
        return up

    # 삭제
    def delete_user_pace_by_id(self, user_pace_id: int) -> UserPaces:
        up = self.user_paces_repository.find_by_id(user_pace_id)
        if not up:
            raise ControlledException(user_paces_error_code.USER_PACE_NOT_FOUND)
        self.user_paces_repository.delete(up)
        self.database.commit()
        return up
