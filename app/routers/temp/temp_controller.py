# app/routers/temp/temp_controller.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.internal.log.log import log
from app.routers.temp.temp_dto import TempBase
from app.routers.temp.temp_service import TempService
from config.common.common_response import CommonResponse
from config.database.postgres_database import get_database

router = APIRouter(prefix="/temp", tags=["temp"])

# - 여기서 Service 인스턴스를 DI로 주입한다.
# - 포인트: 라우터는 비즈니스 로직 모름. 의존성으로 Service만 받아서 호출.
# - Session은 요청 단위로 열고 닫힘(get_database). 메모리 누수 방지.
def get_temp_service(database: Session = Depends(get_database)) -> TempService:
    return TempService(database)        # Service가 트랜잭션/예외 관리 담당

@router.post(
    "",
    response_model=CommonResponse,
    status_code=status.HTTP_200_OK,
)
def calc_paces(paceCreate:TempBase, temp_service: TempService = Depends(get_temp_service)):
    result = temp_service.create_paces(paceCreate)
    return CommonResponse(
        code=200,
        message="페이스 분석 완료",
        data=result
    )