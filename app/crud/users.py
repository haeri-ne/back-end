from typing import Optional

from sqlalchemy.orm import Session

from app.cores.security import get_password_hash
from app.models.users import User
from app.schemas.users import UserCreateRequest, UserResponse
from app.models.roles import Role, RoleEnum


def register(db: Session, user: UserCreateRequest) -> UserResponse:
    """
    새로운 사용자 등록 함수.

    - `username`과 `email`을 사용하여 새로운 사용자를 생성합니다.
    - 비밀번호는 해싱되어 저장됩니다.
    - 기본적으로 `user` 역할을 부여하며, 요청에 따라 `admin` 역할을 부여할 수도 있습니다.

    Args:
        db (Session): 데이터베이스 세션.
        user (UserCreateRequest): 사용자 생성 요청 데이터.

    Returns:
        UserResponse: 생성된 사용자 정보.

    Raises:
        IntegrityError: 동일한 `username` 또는 `email`이 존재하는 경우 예외 발생.
    """
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(new_user)
    db.flush()

    new_role = Role(
        user_id=new_user.id,
        role=RoleEnum.user if user.role == RoleEnum.user else RoleEnum.admin
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_user)
 
    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        role=new_role.role
    )


def get_user(db: Session, username: str) -> Optional[User]:
    """
    사용자 정보 조회 함수.

    - `username`을 기준으로 사용자를 조회합니다.

    Args:
        db (Session): 데이터베이스 세션.
        username (str): 조회할 사용자의 `username`.

    Returns:
        Optional[User]: 사용자가 존재하면 `User` 객체 반환, 없으면 `None` 반환.
    """
    return db.query(User).filter(User.username == username).first()