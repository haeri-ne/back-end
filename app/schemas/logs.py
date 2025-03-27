from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class FrontLogSchema(BaseModel):
    """
    프론트엔드 로그 요청 스키마

    Attributes:
        user_id (str): 로그를 발생시킨 사용자 ID
        event_name (str): 발생한 이벤트 이름
        event_value (Dict[str, Any]): 이벤트에 대한 상세 정보(JSON 형태)
        page_name (Optional[str]): 이벤트가 발생한 페이지 이름
        event_time (datetime): 이벤트 발생 시간
    """
    user_id: str
    event_name: str
    event_value: Dict[str, Any]
    page_name: Optional[str]
    event_time: datetime


class LogResponse(BaseModel):
    """
    로그 저장에 대한 응답 모델

    Attributes:
        status (str): 처리 상태 (기본값: "ok")
        message (str): 응답 메시지 (기본값: "Log received successfully")
    """
    status: str = "ok"
    message: str = "Log received successfully"
