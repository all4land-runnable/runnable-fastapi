# app/routers/pace_records/pace_records_controller.py
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from app.routers.pace_records.pace_records_dto import PaceRecordCreate, PaceRecordUpdate, PaceRecordOut
from app.routers.pace_records.pace_records_repository import PaceRecordsRepository
from app.routers.pace_records.pace_records_service import PaceRecordsService
from config.common.common_response import CommonResponse
from config.database.postgres_database import get_database  # Session 제공

router = APIRouter(prefix="/pace-records", tags=["pace_records"])

def get_pace_records_service(database: Session = Depends(get_database)) -> PaceRecordsService:
    repo = PaceRecordsRepository(database)
    return PaceRecordsService(database, repo)

@router.post("", response_model=CommonResponse[PaceRecordOut], status_code=status.HTTP_201_CREATED)
def create_pace_record(dto: PaceRecordCreate, service: PaceRecordsService = Depends(get_pace_records_service)):
    item = service.create_pace_record(dto)
    return CommonResponse(code=201, message="페이스 기록 생성 성공", data=item)

@router.patch("", response_model=CommonResponse[PaceRecordOut], status_code=status.HTTP_200_OK)
def update_pace_record(dto: PaceRecordUpdate, service: PaceRecordsService = Depends(get_pace_records_service)):
    item = service.update_pace_record(dto)
    return CommonResponse(code=200, message="페이스 기록 수정 성공", data=item)

@router.delete("/{pace_record_id}", response_model=CommonResponse[PaceRecordOut], status_code=status.HTTP_200_OK)
def delete_pace_record(pace_record_id: int, service: PaceRecordsService = Depends(get_pace_records_service)):
    item = service.delete_pace_record_by_id(pace_record_id)
    return CommonResponse(code=200, message="페이스 기록 삭제 성공", data=item)

@router.get("", response_model=CommonResponse[list[PaceRecordOut]], status_code=status.HTTP_200_OK)
def get_all(service: PaceRecordsService = Depends(get_pace_records_service)):
    rows = service.find_all()
    return CommonResponse(code=200, message="페이스 기록 전체 조회 성공", data=rows)

@router.get("/{pace_record_id}", response_model=CommonResponse[PaceRecordOut], status_code=status.HTTP_200_OK)
def read_by_id(pace_record_id: int, service: PaceRecordsService = Depends(get_pace_records_service)):
    item = service.find_by_id(pace_record_id)
    return CommonResponse(code=200, message="페이스 기록 조회 성공", data=item)

@router.get("/record/{record_id}", response_model=CommonResponse[list[PaceRecordOut]], status_code=status.HTTP_200_OK)
def read_by_record_id(record_id: int, service: PaceRecordsService = Depends(get_pace_records_service)):
    rows = service.find_by_record_id(record_id)
    return CommonResponse(code=200, message="페이스 기록(기록별) 조회 성공", data=rows)