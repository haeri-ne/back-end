from fastapi import Request

def get_user_id(request: Request) -> str:
    """
    요청 객체에서 user_id를 추출하는 의존성 함수.

    LoggingMiddleware에서 설정한 `request.state.user_id` 값을 가져오며,
    설정되어 있지 않으면 기본값 "anonymous"를 반환합니다.

    Args:
        request (Request): FastAPI 요청 객체.

    Returns:
        str: 사용자 ID (없을 경우 "anonymous").
    """
    return getattr(request.state, "user_id", "anonymous")
