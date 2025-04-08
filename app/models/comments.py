from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Comment(Base):
    """
    Comment (댓글) 테이블 모델.

    Attributes:
        id (int): 댓글 고유 ID (Primary Key).
        user_id (str): 댓글 작성자의 사용자 ID.
        comment (str): 댓글 내용.
        created_at (date): 댓글 작성 일자.
        menu_id (int): 연결된 메뉴의 ID (Foreign Key).
        menu (Menu): 해당 댓글이 달린 메뉴 객체 (1:N 관계).
    """
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    comment = Column(String, nullable=False)
    created_at = Column(Date, nullable=False)

    menu_id = Column(Integer, ForeignKey("menus.id"))
    menu = relationship("Menu", back_populates="comments", lazy="selectin")

    def __repr__(self):
        """
        댓글 객체 정보를 문자열로 반환합니다.

        Returns:
            str: 댓글 ID, 작성자 ID, 댓글 내용, 작성일자가 포함된 문자열.
        """
        return f"<Comment(id={self.id}, user_id={self.user_id}, comment={self.comment}, created_at={self.created_at})>"
