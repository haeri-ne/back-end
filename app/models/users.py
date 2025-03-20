from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """
    사용자(User) 테이블 모델.

    - `id`: 사용자 고유 ID (PK)
    - `username`: 사용자 로그인 ID
    - `email`: 사용자 이메일 (Unique)
    - `hashed_password`: 해싱된 비밀번호
    - `disabled`: 계정 비활성화 여부 (기본값: `False`)
    - `role`: 사용자 역할 (1:1 관계, `Role` 테이블과 연결됨)
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, doc="사용자 고유 ID")
    username = Column(String, nullable=False, index=True, doc="사용자 로그인 ID")
    email = Column(String, unique=True, nullable=False, index=True, doc="사용자 이메일 (Unique)")
    hashed_password = Column(String, nullable=False, doc="해싱된 비밀번호")
    disabled = Column(Boolean, default=False, doc="계정 비활성화 여부 (기본값: False)")

    role = relationship("Role", back_populates="user", uselist=False, lazy="joined", doc="사용자 역할 (1:1 관계)")

    def __repr__(self):
        """
        객체 정보를 문자열로 반환 (디버깅용).
        """
        return f"<User(id={self.id}, username={self.username}, email={self.email}, role={self.role.role if self.role else 'No Role'})>"
