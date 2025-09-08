# app/routers/sections/sections_controller.py
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from app.routers.sections.sections_dto import SectionCreate, SectionUpdate, SectionOut
from app.routers.sections.sections_repository import SectionsRepository
from app.routers.sections.sections_service import SectionsService
from config.common.common_response import CommonResponse
from config.database.postgres_database import get_database

router = APIRouter(prefix="/sections", tags=["sections"])

# - 여기서 Service 인스턴스를 DI로 주입한다.
# - 포인트: 라우터는 비즈니스 로직 모름. 의존성으로 Service만 받아서 호출.
# - Session은 요청 단위로 열고 닫힘(get_database). 메모리 누수 방지.
def get_sections_service(database: Session = Depends(get_database)) -> SectionsService:
    sections_repository = SectionsRepository(database)        # Repository는 트랜잭션 모름(Commit 금지)
    return SectionsService(database, sections_repository)     # Service가 트랜잭션/예외 관리 담당

# 생성
@router.post(
    "",
    response_model=CommonResponse[SectionOut],
    status_code=status.HTTP_201_CREATED,
)
def create(section_create: SectionCreate, sections_service: SectionsService = Depends(get_sections_service)):
    section = sections_service.create_section(section_create)
    return CommonResponse(code=201, message="섹션 생성 성공", data=section)

# 수정
@router.patch(
    "",
    response_model=CommonResponse[SectionOut],
    status_code=status.HTTP_200_OK,
)
def update(section_update: SectionUpdate, sections_service: SectionsService = Depends(get_sections_service)):
    section = sections_service.update_section(section_update)
    return CommonResponse(code=200, message="섹션 수정 성공", data=section)

# 삭제
@router.delete(
    "/{section_id}",
    response_model=CommonResponse[SectionOut],
    status_code=status.HTTP_200_OK,
)
def delete(section_id: int, sections_service: SectionsService = Depends(get_sections_service)):
    section = sections_service.delete_section_by_id(section_id)
    return CommonResponse(code=200, message="섹션 삭제 성공", data=section)

# 전체 조회
@router.get(
    "",
    response_model=CommonResponse[list[SectionOut]],
    status_code=status.HTTP_200_OK,
)
def get_all(sections_service: SectionsService = Depends(get_sections_service)):
    sections = sections_service.find_all()
    return CommonResponse(code=200, message="섹션 전체 조회 성공", data=sections)

# route_id로 조회
@router.get(
    "/route/{route_id}",
    response_model=CommonResponse[list[SectionOut]],
    status_code=status.HTTP_200_OK,
)
def get_by_route(route_id: int, sections_service: SectionsService = Depends(get_sections_service)):
    sections = sections_service.find_by_route_id(route_id)
    return CommonResponse(code=200, message="섹션 조회 성공", data=sections)

# 개별 조회
@router.get(
    "/{section_id}",
    response_model=CommonResponse[SectionOut],
    status_code=status.HTTP_200_OK,
)
def read_by_id(section_id: int, sections_service: SectionsService = Depends(get_sections_service)):
    section = sections_service.find_by_id(section_id)
    return CommonResponse(code=200, message="섹션 조회 성공", data=section)
