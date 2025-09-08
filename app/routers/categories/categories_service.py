# app/routers/categories/categories_service.py
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.internal.exception.controlled_exception import ControlledException
from app.internal.exception.errorcode import categories_error_code
from app.routers.categories.categories import Categories
from app.routers.categories.categories_dto import CategoryCreate, CategoryUpdate
from app.routers.categories.categories_repository import CategoriesRepository

class CategoriesService:
    def __init__(self, database: Session, categories_repository: CategoriesRepository) -> None:
        # Service는 트랜잭션 경계(Commit/Rollback) + 의미있는 예외 매핑 담당.
        self.database = database
        self.categories_repository = categories_repository

    # 생성
    def create_category(self, category_create: CategoryCreate) -> Categories:
        category = Categories(
            user_id=category_create.user_id,
            name=category_create.name,
        )
        try:
            self.categories_repository.save(category)  # flush까지 하고 PK 확보
            self.database.commit()                     # [핵심] 트랜잭션 확정은 Service에서만
        except IntegrityError as e:
            self.database.rollback()
            # (user_id, name) 유니크 위반 → 비즈니스 에러코드로 변환
            raise ControlledException(category_error_code.DUPLICATE_KEY) from e

        self.database.refresh(category)               # server_default/trigger 동기화
        return category

    # 조회 (없으면 예외)
    def find_by_id(self, category_id: int) -> Categories:
        category = self.categories_repository.find_by_id(category_id)
        if not category:
            raise ControlledException(category_error_code.CATEGORY_NOT_FOUND)
        return category

    def find_by_user_and_name(self, user_id: int, name: str) -> Categories:
        category = self.categories_repository.find_by_user_and_name(user_id, name)
        if not category:
            raise ControlledException(category_error_code.CATEGORY_NOT_FOUND)
        return category

    def find_all(self) -> List[Categories]:
        categories = self.categories_repository.find_all()
        if not categories:
            # 비어있을 때도 예외로 처리하는 패턴을 users에 맞춰 유지
            raise ControlledException(category_error_code.CATEGORY_NOT_FOUND)
        return categories

    # 갱신
    def update_category(self, category_update: CategoryUpdate) -> Categories:
        # 존재 확인부터. 여기서 못 찾으면 아래 로직 전부 스킵.
        category = self.categories_repository.find_by_id(category_update.category_id)
        if not category:
            raise ControlledException(category_error_code.CATEGORY_NOT_FOUND)

        # - 화이트리스트 필드만 반영. 실수로 다른 속성 들어오는 것 차단.
        allowed = {"user_id", "name", "is_deleted"}
        data = category_update.model_dump(exclude_none=True)
        for k, v in data.items():
            if k in allowed and k != "category_id":
                setattr(category, k, v)

        try:
            self.database.commit()
        except IntegrityError as e:
            self.database.rollback()
            # 갱신 중 유니크 위반도 동일하게 매핑
            raise ControlledException(category_error_code.DUPLICATE_KEY) from e
        self.database.refresh(category)
        return category

    # 삭제
    def delete_category_by_id(self, category_id: int) -> Categories:
        category = self.categories_repository.find_by_id(category_id)
        if not category:
            raise ControlledException(category_error_code.CATEGORY_NOT_FOUND)
        self.categories_repository.delete(category)
        self.database.commit()  # delete는 커밋까지 해야 반영
        return category
