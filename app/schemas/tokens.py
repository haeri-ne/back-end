from pydantic import BaseModel

from app.models.roles import RoleEnum


class TokenResponse(BaseModel):
    """
    OAuth2 토큰 응답 모델.

    - `access_token`: 인증된 사용자를 위한 액세스 토큰.
    - `token_type`: 토큰 유형 (보통 "bearer" 사용).
    """
    access_token: str
    token_type: str


class TokenCreateRequest(BaseModel):
    """
    JWT 토큰 생성 요청 모델.

    - `sub`: 사용자 고유 식별자 (보통 username).
    - `role`: 사용자의 역할 (`admin` 또는 `user`).
    """
    sub: str
    role: RoleEnum
