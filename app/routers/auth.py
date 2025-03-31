from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.database import get_db
from app.cores.security import verify_password, create_access_token
from app.crud.users import get_user
from app.schemas.tokens import TokenCreateRequest, TokenResponse


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

router = APIRouter(
    prefix="/auth", 
    tags=["auth"]
)

@router.post("/token", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    사용자 로그인 엔드포인트.

    사용자의 `username`과 `password`를 검증하여 액세스 토큰을 발급합니다.

    Args:
        form_data (OAuth2PasswordRequestForm): 로그인 폼 데이터 (username, password).
        db (Session): 데이터베이스 세션.

    Returns:
        TokenResponse: 발급된 액세스 토큰 및 토큰 유형.

    Raises:
        HTTPException: 로그인 실패 시 `401 Unauthorized` 응답 반환.
    """
    user = get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    token_data = TokenCreateRequest(sub=user.username, role=user.role.role)
    access_token = create_access_token(token_data)
    return TokenResponse(access_token=access_token, token_type="bearer")
