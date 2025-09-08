# app/routers/ranks/ranks_controller.py
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from app.routers.ranks.ranks_dto import RankCreate, RankUpdate, RankOut
from app.routers.ranks.ranks_repository import RanksRepository
from app.routers.ranks.ranks_service import RanksService
from config.common.common_response import CommonResponse
from config.database.postgres_database import get_database  # Session 제공

router = APIRouter(prefix="/ranks", tags=["ranks"])

def get_ranks_service(database: Session = Depends(get_database)) -> RanksService:
    repo = RanksRepository(database)
    return RanksService(database, repo)

@router.post("", response_model=CommonResponse[RankOut], status_code=status.HTTP_201_CREATED)
def create_rank(dto: RankCreate, service: RanksService = Depends(get_ranks_service)):
    item = service.create_rank(dto)
    return CommonResponse(code=201, message="랭크 생성 성공", data=item)

@router.patch("", response_model=CommonResponse[RankOut], status_code=status.HTTP_200_OK)
def update_rank(dto: RankUpdate, service: RanksService = Depends(get_ranks_service)):
    item = service.update_rank(dto)
    return CommonResponse(code=200, message="랭크 수정 성공", data=item)

@router.delete("/{rank_id}", response_model=CommonResponse[RankOut], status_code=status.HTTP_200_OK)
def delete_rank(rank_id: int, service: RanksService = Depends(get_ranks_service)):
    item = service.delete_rank_by_id(rank_id)
    return CommonResponse(code=200, message="랭크 삭제 성공", data=item)

@router.get("", response_model=CommonResponse[list[RankOut]], status_code=status.HTTP_200_OK)
def get_all(service: RanksService = Depends(get_ranks_service)):
    rows = service.find_all()
    return CommonResponse(code=200, message="랭크 전체 조회 성공", data=rows)

@router.get("/{rank_id}", response_model=CommonResponse[RankOut], status_code=status.HTTP_200_OK)
def read_by_id(rank_id: int, service: RanksService = Depends(get_ranks_service)):
    item = service.find_by_id(rank_id)
    return CommonResponse(code=200, message="랭크 조회 성공", data=item)

@router.get("/record/{record_id}", response_model=CommonResponse[list[RankOut]], status_code=status.HTTP_200_OK)
def read_by_record_id(record_id: int, service: RanksService = Depends(get_ranks_service)):
    rows = service.find_by_record_id(record_id)
    return CommonResponse(code=200, message="랭크(기록별) 조회 성공", data=rows)
