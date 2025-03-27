from typing import Any, Dict
from datetime import datetime
from app.cores.logger.config import logger

def record_log(
    user_id: str, 
    request_api: str, 
    status_code: int, 
    response: Dict[str, Any], 
    is_success: bool
) -> None:
    """
    백엔드 로그를 기록하는 함수.

    요청한 사용자 ID, 호출한 API, 응답 상태 코드, 응답 내용 및 성공 여부 등의 정보를
    logger에 기록하며, 로그 핸들러를 통해 DB에 저장할 수 있도록 설정됩니다.

    Args:
        user_id (str): 요청한 사용자 ID.
        request_api (str): 호출한 API 경로.
        status_code (int): HTTP 응답 상태 코드.
        response (Dict[str, Any]): API 응답 데이터.
        is_success (bool): 요청 성공 여부.
    """
    logger.info(
        f"{request_api} 호출",
        extra={
            "user_id": user_id,
            "request_api": request_api,
            "status_code": status_code,
            "response": response,
            "is_success": is_success,
            "time": datetime.now()
        }
    )
