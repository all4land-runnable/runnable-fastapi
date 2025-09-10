# app/routers/points/points_controller.py
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from app.routers.points.points_dto import PointCreate, PointUpdate, PointOut
from app.routers.points.points_repository import PointsRepository
from app.routers.points.points_service import PointsService
from config.common.common_response import CommonResponse
from config.database.postgres_database import get_database

router = APIRouter(prefix="/points", tags=["points"])

# - 여기서 Service 인스턴스를 DI로 주입한다.
# - 포인트: 라우터는 비즈니스 로직 모름. 의존성으로 Service만 받아서 호출.
# - Session은 요청 단위로 열고 닫힘(get_database). 메모리 누수 방지.
def get_points_service(database: Session = Depends(get_database)) -> PointsService:
    points_repository = PointsRepository(database)            # Repository는 트랜잭션 모름(Commit 금지)
    return PointsService(database, points_repository)         # Service가 트랜잭션/예외 관리 담당

# 생성
@router.post(
    "",
    response_model=CommonResponse[PointOut],
    status_code=status.HTTP_201_CREATED,
)
def create(point_create: PointCreate, points_service: PointsService = Depends(get_points_service)):
    point = points_service.create_point(point_create)
    return CommonResponse(code=201, message="포인트 생성 성공", data=point)

# 수정
@router.patch(
    "",
    response_model=CommonResponse[PointOut],
    status_code=status.HTTP_200_OK,
)
def update(point_update: PointUpdate, points_service: PointsService = Depends(get_points_service)):
    point = points_service.update_point(point_update)
    return CommonResponse(code=200, message="포인트 수정 성공", data=point)

# 삭제
@router.delete(
    "/{point_id}",
    response_model=CommonResponse[PointOut],
    status_code=status.HTTP_200_OK,
)
def delete(point_id: int, points_service: PointsService = Depends(get_points_service)):
    point = points_service.delete_point_by_id(point_id)
    return CommonResponse(code=200, message="포인트 삭제 성공", data=point)

# 전체 조회
@router.get(
    "",
    response_model=CommonResponse[list[PointOut]],
    status_code=status.HTTP_200_OK,
)
def get_all(points_service: PointsService = Depends(get_points_service)):
    points = points_service.find_all()
    return CommonResponse(code=200, message="포인트 전체 조회 성공", data=points)

# section_id로 조회
@router.get(
    "/section/{section_id}",
    response_model=CommonResponse[list[PointOut]],
    status_code=status.HTTP_200_OK,
)
def get_by_section(section_id: int, points_service: PointsService = Depends(get_points_service)):
    points = points_service.find_by_section_id(section_id)
    return CommonResponse(code=200, message="포인트 조회 성공", data=points)

# 개별 조회
@router.get(
    "/{point_id}",
    response_model=CommonResponse[PointOut],
    status_code=status.HTTP_200_OK,
)
def read_by_id(point_id: int, points_service: PointsService = Depends(get_points_service)):
    point = points_service.find_by_id(point_id)
    return CommonResponse(code=200, message="포인트 조회 성공", data=point)
