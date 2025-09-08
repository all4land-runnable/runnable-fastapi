# app/routers/categories/categories_controller.py
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from app.routers.categories.categories_dto import CategoryCreate, CategoryUpdate, CategoryOut
from app.routers.categories.categories_repository import CategoriesRepository
from app.routers.categories.categories_service import CategoriesService
from config.common.common_response import CommonResponse
from config.database.postgres_database import get_database  # Session 제공

router = APIRouter(prefix="/categories", tags=["categories"])

# - 여기서 Service 인스턴스를 DI로 주입한다.
# - 포인트: 라우터는 비즈니스 로직 모름. 의존성으로 Service만 받아서 호출.
# - Session은 요청 단위로 열고 닫힘(get_database). 메모리 누수 방지.
def get_categories_service(database: Session = Depends(get_database)) -> CategoriesService:
    categories_repository = CategoriesRepository(database)   # Repository는 트랜잭션 모름(Commit 금지)
    return CategoriesService(database, categories_repository)# Service가 트랜잭션/예외 관리 담당

# 생성
@router.post(
    "",
    response_model=CommonResponse[CategoryOut],
    status_code=status.HTTP_201_CREATED,
)
def create_category(category_create: CategoryCreate, service: CategoriesService = Depends(get_categories_service)):
    # 입력 DTO → Service → DB. 성공 시 201, 응답은 CategoryOut(Pydantic)으로 민감정보 방지.
    category = service.create_category(category_create)
    return CommonResponse(code=201, message="카테고리 생성 성공", data=category)

# 수정
@router.patch(
    "",
    response_model=CommonResponse[CategoryOut],
    status_code=status.HTTP_200_OK,
)
def update(category_update: CategoryUpdate, service: CategoriesService = Depends(get_categories_service)):
    # 부분 수정. 유효성/중복 키는 Service에서 처리.
    category = service.update_category(category_update)
    return CommonResponse(code=200, message="카테고리 수정 성공", data=category)

# 삭제
@router.delete(
    "/{category_id}",
    response_model=CommonResponse[CategoryOut],
    status_code=status.HTTP_200_OK,
)
def delete(category_id: int, service: CategoriesService = Depends(get_categories_service)):
    # id로 삭제. 없으면 ControlledException으로 터뜨림 → 전역 핸들러에서 공통 처리.
    category = service.delete_category_by_id(category_id)
    return CommonResponse(code=200, message="카테고리 삭제 성공", data=category)

# 전체 조회
@router.get(
    "",
    response_model=CommonResponse[list[CategoryOut]],
    status_code=status.HTTP_200_OK,
)
def get_all(service: CategoriesService = Depends(get_categories_service)):
    # 리스트 반환. Service는 단순 위임.
    categories = service.find_all()
    return CommonResponse(code=200, message="카테고리 전체 조회 성공", data=categories)

# 개별 조회들
@router.get(
    "/{category_id}",
    response_model=CommonResponse[CategoryOut],
    status_code=status.HTTP_200_OK,
)
def read_by_id(category_id: int, service: CategoriesService = Depends(get_categories_service)):
    category = service.find_by_id(category_id)
    return CommonResponse(code=200, message="카테고리 조회 성공", data=category)

@router.get(
    "/user/{user_id}/name/{name}",
    response_model=CommonResponse[CategoryOut],
    status_code=status.HTTP_200_OK,
)
def read_by_user_and_name(user_id: int, name: str, service: CategoriesService = Depends(get_categories_service)):
    category = service.find_by_user_and_name(user_id, name)
    return CommonResponse(code=200, message="카테고리 조회 성공", data=category)
