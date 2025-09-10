# app/routers/sections/sections_service.py
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.internal.exception.controlled_exception import ControlledException
from app.internal.exception.errorcode import sections_error_code
from app.routers.sections.sections import Sections
from app.routers.sections.sections_dto import SectionCreate, SectionUpdate
from app.routers.sections.sections_repository import SectionsRepository

class SectionsService:
    def __init__(self, database: Session, sections_repository: SectionsRepository) -> None:
        # Service는 트랜잭션 경계(Commit/Rollback) + 의미있는 예외 매핑 담당.
        self.database = database
        self.sections_repository = sections_repository

    # 생성
    def create_section(self, section_create: SectionCreate) -> Sections:
        section = Sections(
            route_id=section_create.route_id,
            distance=section_create.distance,
            slope=section_create.slope,
        )
        try:
            self.sections_repository.save(section)  # flush까지 하고 PK 확보
            self.database.commit()                  # 트랜잭션 확정은 Service에서만
        except IntegrityError as e:
            self.database.rollback()
            # FK/유니크 위반 등 → 비즈니스 에러코드로 변환
            raise ControlledException(sections_error_code.DUPLICATE_KEY) from e

        self.database.refresh(section)             # server_default/trigger 동기화
        return section

    # 조회 (없으면 예외)
    def find_by_id(self, section_id: int) -> Sections:
        section = self.sections_repository.find_by_id(section_id)
        if not section:
            raise ControlledException(sections_error_code.SECTION_NOT_FOUND)
        return section

    def find_all(self) -> List[Sections]:
        sections = self.sections_repository.find_all()
        if not sections:
            # 빈 리스트를 허용하고 싶다면 이 예외를 제거하세요.
            raise ControlledException(sections_error_code.SECTION_NOT_FOUND)
        return sections

    def find_by_route_id(self, route_id: int) -> List[Sections]:
        sections = self.sections_repository.find_by_route_id(route_id)
        if not sections:
            raise ControlledException(sections_error_code.SECTION_NOT_FOUND)
        return sections

    # 갱신
    def update_section(self, section_update: SectionUpdate) -> Sections:
        section = self.sections_repository.find_by_id(section_update.section_id)
        if not section:
            raise ControlledException(sections_error_code.SECTION_NOT_FOUND)

        # 화이트리스트 필드만 반영
        allowed = {"route_id", "distance", "slope", "is_deleted"}
        data = section_update.model_dump(exclude_none=True)
        for k, v in data.items():
            if k in allowed and k != "section_id":
                setattr(section, k, v)

        try:
            self.database.commit()
        except IntegrityError as e:
            self.database.rollback()
            raise ControlledException(sections_error_code.DUPLICATE_KEY) from e
        self.database.refresh(section)
        return section

    # 삭제
    def delete_section_by_id(self, section_id: int) -> Sections:
        section = self.sections_repository.find_by_id(section_id)
        if not section:
            raise ControlledException(sections_error_code.SECTION_NOT_FOUND)
        self.sections_repository.delete(section)
        self.database.commit()
        return section
