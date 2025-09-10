# app/routers/temp/pace_maker_controller.py
from fastapi import APIRouter, Depends
from starlette import status

from app.routers.pace_maker.pace_maker_dto import PaceMakerDTO
from app.routers.pace_maker.pace_maker_service import PaceMakerService
from config.common.common_response import CommonResponse

router = APIRouter(prefix="/pace_maker", tags=["pace_maker"])

# - 여기서 Service 인스턴스를 DI로 주입한다.
# - 포인트: 라우터는 비즈니스 로직 모름. 의존성으로 Service만 받아서 호출.
# - Session은 요청 단위로 열고 닫힘(get_database). 메모리 누수 방지.
def get_pace_maker_service() -> PaceMakerService:
    return PaceMakerService()        # Service가 트랜잭션/예외 관리 담당

@router.post(
    "",
    response_model=CommonResponse,
    status_code=status.HTTP_200_OK,
)
def calc_paces2(paceCreate:PaceMakerDTO, pace_maker_service: PaceMakerService = Depends(get_pace_maker_service)):
    result = pace_maker_service.pace_maker(paceCreate)
    return CommonResponse(
        code=200,
        message="페이스 분석 완료",
        data=result
    )