from typing import List

from sqlalchemy.orm import Session

from app.schemas.logs import FrontLogSchema, LogResponse
from app.models.logs import FrontLog

def save_logs(db: Session, log_list: List[FrontLogSchema]) -> LogResponse:
    """
    프론트엔드에서 전달받은 로그를 데이터베이스에 저장합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        log_list (List[FrontLogSchema]): 프론트엔드 로그 정보 (사용자 ID, 이벤트명 등).

    Returns:
        LogResponse: 로그 저장 성공 응답 객체.
    """
    
    for log in log_list:
        new_log = FrontLog(
            user_id=log.user_id,
            event_name=log.event_name,
            event_value=log.event_value,
            page_name=log.page_name,
            event_time=log.event_time
        )

        db.add(new_log)

    return LogResponse()
