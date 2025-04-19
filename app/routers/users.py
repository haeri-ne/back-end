from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.crud import users
from app.schemas.users import UserCreateRequest, UserResponse

router = APIRouter(
    prefix="/users", 
    tags=["users"]
)

@router.post("/register")
async def register(
    user: UserCreateRequest,
    db: Session = Depends(get_db)
):
    """
    새로운 사용자 등록 API.

    - 입력된 `username`이 이미 존재하는 경우 예외 발생.
    - 비밀번호는 해싱되어 저장됨.

    Args:
        user (UserCreateRequest): 사용자 생성 요청 데이터.
        db (Session): 데이터베이스 세션.

    Returns:
        UserResponse: 생성된 사용자 정보.

    Raises:
        HTTPException: 이미 존재하는 `username`일 경우 400 Bad Request 반환.
    """
    existing_user = users.get_user(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = users.register(db, user)
    return UserResponse.model_validate(new_user)


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """
    현재 로그인한 사용자 정보 조회 API.

    - 액세스 토큰을 통해 인증된 사용자 정보를 반환.

    Args:
        current_user (UserResponse): 현재 인증된 사용자.

    Returns:
        UserResponse: 현재 로그인한 사용자 정보.
    """
    return current_user
