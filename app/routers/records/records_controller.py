# app/routers/records/records_controller.py
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from app.routers.records.records_dto import RecordCreate, RecordUpdate, RecordOut
from app.routers.records.records_repository import RecordsRepository
from app.routers.records.records_service import RecordsService
from config.common.common_response import CommonResponse
from config.database.postgres_database import get_database  # Session 제공

router = APIRouter(prefix="/records", tags=["records"])

# - 여기서 Service 인스턴스를 DI로 주입한다.
# - 포인트: 라우터는 비즈니스 로직 모름. 의존성으로 Service만 받아서 호출.
# - Session은 요청 단위로 열고 닫힘(get_database). 메모리 누수 방지.
def get_records_service(database: Session = Depends(get_database)) -> RecordsService:
    repo = RecordsRepository(database)                  # Repository는 트랜잭션 모름(Commit 금지)
    return RecordsService(database, repo)               # Service가 트랜잭션/예외 관리 담당

# 생성
@router.post(
    "",
    response_model=CommonResponse[RecordOut],
    status_code=status.HTTP_201_CREATED,
)
def create_record(dto: RecordCreate, service: RecordsService = Depends(get_records_service)):
    rec = service.create_record(dto)
    return CommonResponse(code=201, message="기록 생성 성공", data=rec)

# 수정
@router.patch(
    "",
    response_model=CommonResponse[RecordOut],
    status_code=status.HTTP_200_OK,
)
def update(dto: RecordUpdate, service: RecordsService = Depends(get_records_service)):
    rec = service.update_record(dto)
    return CommonResponse(code=200, message="기록 수정 성공", data=rec)

# 삭제
@router.delete(
    "/{record_id}",
    response_model=CommonResponse[RecordOut],
    status_code=status.HTTP_200_OK,
)
def delete(record_id: int, service: RecordsService = Depends(get_records_service)):
    rec = service.delete_record_by_id(record_id)
    return CommonResponse(code=200, message="기록 삭제 성공", data=rec)

# 전체 조회
@router.get(
    "",
    response_model=CommonResponse[list[RecordOut]],
    status_code=status.HTTP_200_OK,
)
def get_all(service: RecordsService = Depends(get_records_service)):
    rows = service.find_all()
    return CommonResponse(code=200, message="기록 전체 조회 성공", data=rows)

# 개별 조회
@router.get(
    "/{record_id}",
    response_model=CommonResponse[RecordOut],
    status_code=status.HTTP_200_OK,
)
def read_by_id(record_id: int, service: RecordsService = Depends(get_records_service)):
    rec = service.find_by_id(record_id)
    return CommonResponse(code=200, message="기록 조회 성공", data=rec)

# user_route별 조회
@router.get(
    "/user-route/{user_route_id}",
    response_model=CommonResponse[list[RecordOut]],
    status_code=status.HTTP_200_OK,
)
def read_by_user_route(user_route_id: int, service: RecordsService = Depends(get_records_service)):
    rows = service.find_by_user_route_id(user_route_id)
    return CommonResponse(code=200, message="기록(루트별) 조회 성공", data=rows)
