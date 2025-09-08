# app/routers/user_strategies/user_strategies_controller.py
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from app.routers.user_strategies.user_strategies_dto import UserStrategyCreate, UserStrategyUpdate, UserStrategyOut
from app.routers.user_strategies.user_strategies_repository import UserStrategiesRepository
from app.routers.user_strategies.user_strategies_service import UserStrategiesService
from config.common.common_response import CommonResponse
from config.database.postgres_database import get_database  # Session 제공

router = APIRouter(prefix="/user-strategies", tags=["user_strategies"])

# - 여기서 Service 인스턴스를 DI로 주입한다.
# - 포인트: 라우터는 비즈니스 로직 모름. 의존성으로 Service만 받아서 호출.
# - Session은 요청 단위로 열고 닫힘(get_database). 메모리 누수 방지.
def get_user_strategies_service(database: Session = Depends(get_database)) -> UserStrategiesService:
    repo = UserStrategiesRepository(database)              # Repository는 트랜잭션 모름(Commit 금지)
    return UserStrategiesService(database, repo)           # Service가 트랜잭션/예외 관리 담당

# 생성
@router.post(
    "",
    response_model=CommonResponse[UserStrategyOut],
    status_code=status.HTTP_201_CREATED,
)
def create_user_strategy(dto: UserStrategyCreate, service: UserStrategiesService = Depends(get_user_strategies_service)):
    # 입력 DTO → Service → DB. 성공 시 201, 응답은 UserStrategyOut(Pydantic)
    us = service.create_user_strategy(dto)
    return CommonResponse(code=201, message="유저-루트 전략 생성 성공", data=us)

# 수정
@router.patch(
    "",
    response_model=CommonResponse[UserStrategyOut],
    status_code=status.HTTP_200_OK,
)
def update(dto: UserStrategyUpdate, service: UserStrategiesService = Depends(get_user_strategies_service)):
    # 부분 수정. 유효성/중복 키는 Service에서 처리.
    us = service.update_user_strategy(dto)
    return CommonResponse(code=200, message="유저-루트 전략 수정 성공", data=us)

# 삭제
@router.delete(
    "/{user_strategy_id}",
    response_model=CommonResponse[UserStrategyOut],
    status_code=status.HTTP_200_OK,
)
def delete(user_strategy_id: int, service: UserStrategiesService = Depends(get_user_strategies_service)):
    # id로 삭제. 없으면 ControlledException으로 터뜨림 → 전역 핸들러에서 공통 처리.
    us = service.delete_user_strategy_by_id(user_strategy_id)
    return CommonResponse(code=200, message="유저-루트 전략 삭제 성공", data=us)

# 전체 조회
@router.get(
    "",
    response_model=CommonResponse[list[UserStrategyOut]],
    status_code=status.HTTP_200_OK,
)
def get_all(service: UserStrategiesService = Depends(get_user_strategies_service)):
    # 리스트 반환. Service는 단순 위임.
    items = service.find_all()
    return CommonResponse(code=200, message="유저-루트 전략 전체 조회 성공", data=items)

# 개별 조회
@router.get(
    "/{user_strategy_id}",
    response_model=CommonResponse[UserStrategyOut],
    status_code=status.HTTP_200_OK,
)
def read_by_id(user_strategy_id: int, service: UserStrategiesService = Depends(get_user_strategies_service)):
    # 동적 파라미터는 맨 마지막. 경로 충돌 방지.
    us = service.find_by_id(user_strategy_id)
    return CommonResponse(code=200, message="유저-루트 전략 조회 성공", data=us)
