from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.routers.pace.paces_dto import PaceBase
from app.routers.pace.paces_service import PacesService
from config.common.common_response import CommonResponse
from config.database.postgres_database import get_database

router = APIRouter(prefix="/paces", tags=["paces"])

# - 여기서 Service 인스턴스를 DI로 주입한다.
# - 포인트: 라우터는 비즈니스 로직 모름. 의존성으로 Service만 받아서 호출.
# - Session은 요청 단위로 열고 닫힘(get_database). 메모리 누수 방지.
def get_paces_service(database: Session = Depends(get_database)) -> PacesService:
    return PacesService(database)        # Service가 트랜잭션/예외 관리 담당

@router.post(
    "",
    response_model=CommonResponse[PaceBase],
    status_code=status.HTTP_201_CREATED,
)
def create_pace(pace_base: PaceBase, paces_service: PacesService = Depends(get_paces_service)):
    """
    요약:
        AI와 대화하는 API

    설명:
        main_llm에서 전체 채팅이 반환되면 response가 반환됩니다.

    Parameters:
        body(ChatRequest): 사용자의 답변에 필요한 인자의 모음
            * message, user_id, ego_id를 Attributes로 갖는다.
            :param pace_base:
            :param paces_service:
    """
    # NOTE: 에고 채팅 생성
    pace = paces_service.chat(pace_base)

    return CommonResponse(  # 성공 시, Code 200을 반환합니다. 예외처리는 chat_stream을 참고해주세요.
        code=201,
        message="답변 전송 완료",
        data=pace
    )