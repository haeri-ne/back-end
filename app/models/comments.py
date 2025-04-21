from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Comment(Base):
    """
    Comment (댓글) 테이블 모델.

    Attributes:
        id (Integer): 댓글 고유 ID (Primary Key)
        user_id (String(100)): 사용자 식별자 (UUID)
        comment (String(255)): 댓글 내용
        created_at (DateTime): 댓글 작성 일자
        menu_id (Integer): 연결된 메뉴 ID (Foreign Key)
        menu (Menu): 해당 댓글이 달린 메뉴 객체 (1:N 관계)
    """
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), nullable=False)
    comment = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)

    menu_id = Column(Integer, ForeignKey("menus.id"))
    menu = relationship("Menu", back_populates="comments", lazy="selectin")

    def __repr__(self):
        """객체 정보를 문자열로 반환 (디버깅용)."""
        return f"<Comment(id={self.id}, user_id={self.user_id}, comment={self.comment}, created_at={self.created_at})>"
