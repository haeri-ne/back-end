import json

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.cores.logger.logger import record_log


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    HTTP 요청 및 응답을 로깅하는 미들웨어.

    요청 시 user-id 헤더 값을 확인하고, API 경로 및 응답 상태 코드를 포함한 로그를 기록합니다.
    응답 본문이 JSON일 경우 디코딩하여 응답 데이터까지 로그에 포함하며,
    상태 코드가 400 이상인 경우 is_success 플래그를 False로 기록합니다.

    Attributes:
        EXCLUDE_PATH (List[str]): 로깅에서 제외할 경로 목록 (헬스체크, 문서 등).
    """
    EXCLUDE_PATH = ["/health", "/openapi.json", "/api/v1/health", "/favicon.ico"]

    async def dispatch(self, request: Request, call_next):
        """
        요청-응답을 가로채어 로그를 기록합니다.

        Args:
            request (Request): 클라이언트의 요청 객체.
            call_next (Callable): 다음 미들웨어 혹은 라우터를 호출하는 함수.

        Returns:
            Response: 가공되거나 원본 그대로인 응답 객체.

        Raises:
            Exception: 내부 처리 중 예외 발생 시 그대로 전달.
        """
        user_id = request.headers.get("user-id", "anonymous")
        request_api = f"{request.method} {request.url.path}"
        request.state.user_id = user_id

        try:
            response = await call_next(request)

            chunks = []
            async for chunk in response.body_iterator:
                chunks.append(chunk)
            response_body = b''.join(chunks)

            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )

            decoded_body = response_body.decode("utf-8")
            if decoded_body.strip() and request.url.path not in self.EXCLUDE_PATH:
                try:
                    response_data = json.loads(decoded_body)
                    record_log(
                        user_id=user_id,
                        request_api=request_api,
                        status_code=response.status_code,
                        response=response_data,
                        is_success=response.status_code < 400
                    )
                except json.JSONDecodeError:
                    pass

            return response

        except Exception as e:
            raise
