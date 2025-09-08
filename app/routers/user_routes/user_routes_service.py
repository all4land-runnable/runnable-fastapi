# app/routers/user_routes/user_routes_service.py
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.internal.exception.controlled_exception import ControlledException
from app.internal.exception.errorcode import user_routes_error_code
from app.routers.user_routes.user_routes import UserRoutes
from app.routers.user_routes.user_routes_dto import UserRouteCreate, UserRouteUpdate
from app.routers.user_routes.user_routes_repository import UserRoutesRepository

class UserRoutesService:
    def __init__(self, database: Session, user_routes_repository: UserRoutesRepository) -> None:
        # Service는 트랜잭션 경계(Commit/Rollback) + 의미있는 예외 매핑 담당.
        self.database = database
        self.user_routes_repository = user_routes_repository

    # 생성
    def create_user_route(self, dto: UserRouteCreate) -> UserRoutes:
        ur = UserRoutes(
            user_id=dto.user_id,
            category_id=dto.category_id,
            route_id=dto.route_id,
        )
        try:
            self.user_routes_repository.save(ur) # flush까지 하고 PK 확보
            self.database.commit()               # [핵심] 트랜잭션 확정은 Service에서만
        except IntegrityError as e:
            self.database.rollback()
            # 중복 키(유니크 위반) 비즈니스 에러코드로 변환
            raise ControlledException(user_routes_error_code.DUPLICATE_KEY) from e

        self.database.refresh(ur)               # server_default/trigger 동기화
        return ur

    # 조회 (없으면 예외)
    def find_by_id(self, user_route_id: int) -> UserRoutes:
        ur = self.user_routes_repository.find_by_id(user_route_id)
        if not ur:
            raise ControlledException(user_routes_error_code.USER_ROUTE_NOT_FOUND)
        return ur

    def find_all(self) -> List[UserRoutes]:
        urs = self.user_routes_repository.find_all()
        if not urs:
            raise ControlledException(user_routes_error_code.USER_ROUTE_NOT_FOUND)
        return urs

    # 갱신
    def update_user_route(self, dto: UserRouteUpdate) -> UserRoutes:
        ur = self.user_routes_repository.find_by_id(dto.user_route_id)
        if not ur:
            raise ControlledException(user_routes_error_code.USER_ROUTE_NOT_FOUND)

        # [명준 주석]
        # - 화이트리스트 필드만 반영. 실수로 다른 속성 들어오는 것 차단.
        allowed = {"user_id", "category_id", "route_id", "is_deleted"}
        data = dto.model_dump(exclude_none=True)
        for k, v in data.items():
            if k in allowed and k != "user_route_id":
                setattr(ur, k, v)

        try:
            self.database.commit()
        except IntegrityError as e:
            self.database.rollback()
            # 갱신 중 유니크 위반도 동일하게 매핑
            raise ControlledException(user_routes_error_code.DUPLICATE_KEY) from e
        self.database.refresh(ur)
        return ur

    # 삭제
    def delete_user_route_by_id(self, user_route_id: int) -> UserRoutes:
        ur = self.user_routes_repository.find_by_id(user_route_id)
        if not ur:
            raise ControlledException(user_route_error_code.USER_ROUTE_NOT_FOUND)
        self.user_routes_repository.delete(ur)
        self.database.commit()  # delete는 커밋까지 해야 반영
        return ur
