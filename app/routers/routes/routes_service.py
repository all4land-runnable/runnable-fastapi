# app/routers/routes/routes_service.py
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.internal.exception.controlled_exception import ControlledException
from app.internal.exception.errorcode import route_error_code
from app.routers.routes.routes import Routes
from app.routers.routes.routes_dto import RouteCreate, RouteUpdate
from app.routers.routes.routes_repository import RoutesRepository

class RoutesService:
    def __init__(self, database: Session, routes_repository: RoutesRepository) -> None:
        # Service는 트랜잭션 경계(Commit/Rollback) + 의미있는 예외 매핑 담당.
        self.database = database
        self.routes_repository = routes_repository

    # 생성
    def create_route(self, route_create: RouteCreate) -> Routes:
        route = Routes(
            title=route_create.title,
            description=route_create.description,
            distance=route_create.distance,
            high_height=route_create.high_height,
            low_height=route_create.low_height,
        )
        try:
            self.routes_repository.save(route) # flush까지 하고 PK 확보
            self.database.commit() # [핵심] 트랜잭션 확정은 Service에서만
        except IntegrityError as e:
            self.database.rollback()
            # (현재 유니크 제약은 없지만, 제약 위반 등 DB 오류를 공통 코드로 매핑)
            raise ControlledException(route_error_code.DUPLICATE_KEY) from e
        self.database.refresh(route) # server_default/trigger 동기화
        return route

    # 조회 (없으면 예외)
    def find_by_id(self, route_id: int) -> Routes:
        # Optional → 존재 보장으로 승격(없으면 예외)
        route = self.routes_repository.find_by_id(route_id)
        if not route:
            raise ControlledException(route_error_code.ROUTE_NOT_FOUND)
        return route

    def find_all(self) -> List[Routes]:
        routes = self.routes_repository.find_all()
        if not routes:
            # 리스트가 비어도 도메인 예외로 처리(사용자 경험 통일)
            raise ControlledException(route_error_code.ROUTE_NOT_FOUND)
        return routes

    # 갱신
    def update_route(self, route_update: RouteUpdate) -> Routes:
        # 존재 확인부터. 여기서 못 찾으면 아래 로직 전부 스킵.
        route = self.routes_repository.find_by_id(route_update.route_id)
        if not route:
            raise ControlledException(route_error_code.ROUTE_NOT_FOUND)

        # - 화이트리스트 필드만 반영. 실수로 다른 속성 들어오는 것 차단.
        allowed = {"title", "description", "distance", "high_height", "low_height", "is_deleted"}
        data = route_update.model_dump(exclude_none=True)  # None 값들은 아예 제외
        for k, v in data.items():
            if k in allowed and k != "route_id":
                setattr(route, k, v)

        try:
            self.database.commit()
        except IntegrityError as e:
            self.database.rollback()
            # 갱신 중 제약 위반도 동일하게 매핑
            raise ControlledException(route_error_code.DUPLICATE_KEY) from e
        self.database.refresh(route)
        return route

    # 삭제
    def delete_route_by_id(self, route_id: int) -> Routes:
        # 먼저 존재 확인 → 없으면 도메인 예외
        route = self.routes_repository.find_by_id(route_id)
        if not route:
            raise ControlledException(route_error_code.ROUTE_NOT_FOUND)
        self.routes_repository.delete(route)
        self.database.commit()  # delete는 커밋까지 해야 반영
        return route
