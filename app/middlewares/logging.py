import json

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.cores.logger.logger import record_log


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    HTTP 요청 및 응답을 로깅하는 미들웨어.

    요청 시 user-id 헤더 값을 추출하여 요청 상태에 저장하며,
    API 경로, 요청 헤더, 요청 본문, 응답 상태 코드, 응답 본문 등을 로그에 기록합니다.

    응답 본문이 JSON일 경우 디코딩하여 구조화된 응답으로 기록하고,
    상태 코드가 400 이상이면 `is_success`를 False로 기록합니다.

    Attributes:
        EXCLUDE_PATH (List[str]): 로깅 대상에서 제외할 경로 목록 (헬스체크, Swagger 등).
    """
    EXCLUDE_PATH = ["/health", "/openapi.json", "/api/v1/health", "/favicon.ico"]

    async def dispatch(self, request: Request, call_next):
        """
        HTTP 요청과 응답을 가로채어 로깅 처리합니다.

        Args:
            request (Request): Starlette Request 객체.
            call_next (Callable): 다음 처리 미들웨어 또는 라우터 함수.

        Returns:
            Response: 원본 혹은 가공된 Starlette Response 객체.
        """
        user_id = request.headers.get("user-id", "anonymous")
        request_api = f"{request.method} {request.url.path}"
        request.state.user_id = user_id

        try:
            request_body = await request.body()
            request_body_decoded = request_body.decode("utf-8") if request_body else None
            
            request._receive = lambda: {"type": "http.request", "body": request_body}

            response = await call_next(request)

            chunks = []
            async for chunk in response.body_iterator:
                chunks.append(chunk)
            response_body = b"".join(chunks)

            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )

            decoded_body = response_body.decode("utf-8")
            if decoded_body.strip() and request.url.path not in self.EXCLUDE_PATH:
                try:
                    record_log(
                        user_id=user_id,
                        request_api=request_api,
                        request_header=json.loads(json.dumps(dict(request.headers))) if request.headers else None,
                        request_body=json.loads(request_body_decoded) if request_body_decoded else None,
                        status_code=response.status_code,
                        response=json.loads(decoded_body),
                        is_success=response.status_code < 400
                    )
                except json.JSONDecodeError:
                    pass

            return response

        except Exception as e:
            raise
