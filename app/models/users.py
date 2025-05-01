from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """
    사용자(User) 테이블 모델.

    Attributes:
        id (Integer): 사용자 고유 ID (Primary Key)
        username (String(100)): 사용자 로그인 ID
        email (String(100)): 사용자 이메일
        hashed_password (String(255)): 해싱된 비밀번호
        disabled (Boolean): 계정 비활성화 여부 (기본값: `False`)
        role (Role): 사용자 역할 (1:1 관계)
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    disabled = Column(Boolean, default=False)

    role = relationship("Role", back_populates="user", uselist=False, lazy="joined")

    def __repr__(self):
        """객체 정보를 문자열로 반환 (디버깅용)."""
        return f"<User(id={self.id}, username={self.username}, email={self.email}, role={self.role.role if self.role else 'No Role'})>"
