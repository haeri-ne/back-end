from enum import Enum
from sqlalchemy import Column, Integer, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class RoleEnum(str, Enum):
    """
    역할(Role) Enum.

    Attributes:
        admin: 관리자 역할
        user: 일반 사용자 역할
    """
    admin = "admin"
    user = "user"


class Role(Base):
    """
    역할(Role) 테이블 모델.

    Attributes:
        id (Integer): 역할 고유 ID (Primary Key)
        role (SQLAlchemyEnum(RoleEnum)): 사용자 역할 (`admin` or `user`)
        user_id (Integer): 역할을 가진 사용자 ID (Foreign Key)
        user (User): 해댱 역할을 가진 사용자 객체 (1:1 관계)
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(SQLAlchemyEnum(RoleEnum), nullable=False, doc="사용자의 역할 (admin/user)")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, doc="사용자 ID")
    user = relationship("User", back_populates="role", lazy="joined")

    def __repr__(self):
        """객체 정보를 문자열로 반환 (디버깅용)."""
        return f"<Role(id={self.id}, role={self.role}, user_id={self.user_id})>"
