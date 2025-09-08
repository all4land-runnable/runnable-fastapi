# app/routers/available_times/available_times_controller.py
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from app.routers.available_times.available_times_dto import (
    AvailableTimeCreate, AvailableTimeUpdate, AvailableTimeOut
)
from app.routers.available_times.available_times_repository import AvailableTimesRepository
from app.routers.available_times.available_times_service import AvailableTimesService
from config.common.common_response import CommonResponse
from config.database.postgres_database import get_database  # Session 제공

router = APIRouter(prefix="/available-times", tags=["available_times"])

# - 여기서 Service 인스턴스를 DI로 주입한다.
# - 포인트: 라우터는 비즈니스 로직 모름. 의존성으로 Service만 받아서 호출.
# - Session은 요청 단위로 열고 닫힘(get_database). 메모리 누수 방지.
def get_available_times_service(database: Session = Depends(get_database)) -> AvailableTimesService:
    repo = AvailableTimesRepository(database)               # Repository는 트랜잭션 모름(Commit 금지)
    return AvailableTimesService(database, repo)            # Service가 트랜잭션/예외 관리 담당

# 생성
@router.post(
    "",
    response_model=CommonResponse[AvailableTimeOut],
    status_code=status.HTTP_201_CREATED,
)
def create_available_time(dto: AvailableTimeCreate, service: AvailableTimesService = Depends(get_available_times_service)):
    # 입력 DTO → Service → DB. 성공 시 201, 응답은 AvailableTimeOut(Pydantic)
    item = service.create_available_time(dto)
    return CommonResponse(code=201, message="이용 가능 시간 생성 성공", data=item)

# 수정
@router.patch(
    "",
    response_model=CommonResponse[AvailableTimeOut],
    status_code=status.HTTP_200_OK,
)
def update(dto: AvailableTimeUpdate, service: AvailableTimesService = Depends(get_available_times_service)):
    # 부분 수정. 유효성/중복 키는 Service에서 처리.
    item = service.update_available_time(dto)
    return CommonResponse(code=200, message="이용 가능 시간 수정 성공", data=item)

# 삭제
@router.delete(
    "/{available_time_id}",
    response_model=CommonResponse[AvailableTimeOut],
    status_code=status.HTTP_200_OK,
)
def delete(available_time_id: int, service: AvailableTimesService = Depends(get_available_times_service)):
    # id로 삭제. 없으면 ControlledException으로 터뜨림 → 전역 핸들러에서 공통 처리.
    item = service.delete_available_time_by_id(available_time_id)
    return CommonResponse(code=200, message="이용 가능 시간 삭제 성공", data=item)

# 전체 조회
@router.get(
    "",
    response_model=CommonResponse[list[AvailableTimeOut]],
    status_code=status.HTTP_200_OK,
)
def get_all(service: AvailableTimesService = Depends(get_available_times_service)):
    # 리스트 반환. Service는 단순 위임.
    items = service.find_all()
    return CommonResponse(code=200, message="이용 가능 시간 전체 조회 성공", data=items)

# 개별 조회 (by id)
@router.get(
    "/{available_time_id}",
    response_model=CommonResponse[AvailableTimeOut],
    status_code=status.HTTP_200_OK,
)
def read_by_id(available_time_id: int, service: AvailableTimesService = Depends(get_available_times_service)):
    # 동적 파라미터는 맨 마지막. 경로 충돌 방지.
    item = service.find_by_id(available_time_id)
    return CommonResponse(code=200, message="이용 가능 시간 조회 성공", data=item)

# 라우트별 조회
@router.get(
    "/route/{route_id}",
    response_model=CommonResponse[list[AvailableTimeOut]],
    status_code=status.HTTP_200_OK,
)
def read_by_route_id(route_id: int, service: AvailableTimesService = Depends(get_available_times_service)):
    items = service.find_by_route_id(route_id)
    return CommonResponse(code=200, message="이용 가능 시간(루트별) 조회 성공", data=items)
