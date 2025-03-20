from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.database import get_db
from app.cores.security import SECRET_KEY, ALGORITHM
from app.crud.users import get_user
from app.models.users import User
from app.models.roles import RoleEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    현재 사용자를 JWT 토큰을 통해 검증 후 반환.

    Args:
        token (str): 요청에서 전달된 JWT 토큰.
        db (Session): 데이터베이스 세션.

    Returns:
        User: 인증된 사용자 객체.

    Raises:
        HTTPException: 토큰이 없거나, 유효하지 않거나, 사용자가 존재하지 않을 경우.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        user = get_user(db, username)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    관리자 권한을 가진 사용자만 접근 가능하도록 검증.

    Args:
        current_user (User): 현재 인증된 사용자.

    Returns:
        User: 관리자 권한이 확인된 사용자 객체.

    Raises:
        HTTPException: 사용자가 관리자 권한이 없을 경우 `403 Forbidden` 예외 발생.
    """
    if current_user.role.role != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admins only.",
        )
    return current_user
