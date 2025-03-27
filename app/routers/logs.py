from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.crud import logs
from app.database import get_db
from app.schemas.logs import FrontLogSchema, LogResponse

router = APIRouter(
    prefix="/logs",
    tags=["logs"],
    responses={404: {"description": "Not found"}},
)

@router.post("/front", response_model=LogResponse, status_code=status.HTTP_201_CREATED)
async def receive_front_log(
    log: FrontLogSchema,
    db: Session = Depends(get_db)
):
    """
    프론트엔드 로그 수신 API

    프론트엔드에서 발생한 사용자 이벤트 로그를 서버로 전송하고 저장합니다.

    Args:
        log (FrontLogSchema): 프론트 로그 데이터(JSON)
        db (Session): 데이터베이스 세션

    Returns:
        LogResponse: 로그 저장 성공 응답
    """
    return logs.save_logs(db, log)
