# app/routers/categories/categories_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.routers.categories.categories import Categories

class CategoriesRepository:
    def __init__(self, database: Session) -> None:
        # Repository는 DB 접근 전용. 트랜잭션(Commit/Rollback) 모름.
        self.database = database

    # 트랜잭션은 Service가 관리 → 여기선 commit() 하지 않음
    def save(self, category: Categories) -> Categories:
        # add로 pending에 올리고, flush로 즉시 INSERT 실행 + PK 확보.
        self.database.add(category)
        self.database.flush()   # PK 확보/조기 예외 감지
        return category

    def find_by_id(self, category_id: int) -> Optional[Categories]:
        # PK 조회 최단코스. 없으면 None.
        return self.database.get(Categories, category_id)

    def find_by_user_and_name(self, user_id: int, name: str) -> Optional[Categories]:
        # 유저 내 이름 유니크 가정. 0/1 건만 나와야 함.
        return self.database.execute(
            select(Categories).where(
                Categories.user_id == user_id,
                Categories.name == name
            )
        ).scalar_one_or_none()

    def find_all(self) -> List[Categories]:
        # 전체 조회. scalars()로 엔티티 컬럼만 뽑고, all() → list 캐스팅.
        return list(self.database.execute(select(Categories)).scalars().all())

    def delete(self, category: Categories) -> None:
        # 삭제는 Service에서 commit으로 마무리.
        self.database.delete(category)

    def delete_by_id(self, category_id: int) -> bool:
        # 편의용. True면 삭제 예정 상태, 커밋은 Service에서.
        category = self.find_by_id(category_id)
        if not category:
            return False
        self.database.delete(category)
        return True
