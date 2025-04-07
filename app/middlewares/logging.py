import json

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.cores.logger.logger import record_log


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    모든 HTTP 요청 및 응답을 로깅하는 미들웨어.

    - 요청 시 user-id 헤더를 확인하고 API 엔드포인트, 응답 상태코드 등을 기록합니다.
    - 응답 바디가 JSON 형식일 경우 디코딩하여 응답 내용을 함께 저장합니다.
    - 비정상 응답(예: status >= 400)도 is_success 플래그로 기록됩니다.
    """
    EXCLUDE_PATH = ["/health", "/openapi.json", "/api/v1/health", "/favicon.ico"]

    async def dispatch(self, request: Request, call_next):
        user_id = request.headers.get("user-id", "anonymous")
        request_api = f"{request.method} {request.url.path}"

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
            if decoded_body.strip() and request.url.path not in self.UNINCLUDE_PATH:
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
