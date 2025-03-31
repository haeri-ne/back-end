from datetime import datetime, timedelta

import bcrypt
from jose import jwt

from app.config import get_settings
from app.schemas.tokens import TokenCreateRequest

settings = get_settings()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def get_password_hash(password: str) -> str:
    """
    주어진 비밀번호를 해싱하여 반환.

    Args:
        password (str): 사용자의 원본 비밀번호.

    Returns:
        str: 해싱된 비밀번호.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    사용자가 입력한 비밀번호가 저장된 해시 값과 일치하는지 확인.

    Args:
        plain_password (str): 사용자가 입력한 원본 비밀번호.
        hashed_password (str): 데이터베이스에 저장된 해싱된 비밀번호.

    Returns:
        bool: 비밀번호가 일치하면 `True`, 그렇지 않으면 `False`.
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def create_access_token(data: TokenCreateRequest) -> str:
    """
    사용자 정보를 기반으로 JWT 액세스 토큰을 생성.

    Args:
        data (TokenCreateRequest): JWT에 포함할 사용자 정보 (`sub`, `role`, `exp`).

    Returns:
        str: 생성된 JWT 액세스 토큰.
    """
    to_encode = {
        "sub": data.sub,
        "role": data.role,
        "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
