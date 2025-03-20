from pydantic import BaseModel, ConfigDict
from app.models.roles import RoleEnum

class UserResponse(BaseModel):
    """
    사용자 정보 응답 모델.

    - `id`: 사용자 고유 ID.
    - `username`: 사용자 로그인 ID.
    - `email`: 사용자 이메일.
    - `role`: 사용자 역할 (`admin` 또는 `user`).
    """
    id: int
    username: str
    email: str
    role: RoleEnum 

    model_config = ConfigDict(from_attributes=True)

class UserCreateRequest(BaseModel):
    """
    사용자 생성 요청 모델.

    - `username`: 사용자 로그인 ID.
    - `email`: 사용자 이메일.
    - `password`: 사용자 비밀번호.
    - `role`: 사용자 역할 (`admin` 또는 `user`).
    """
    username: str
    email: str
    password: str
    role: RoleEnum

    model_config = ConfigDict(use_enum_values=True)
