from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Vote(Base):
    """
    투표(Vote) 테이블 모델.

    Attributes:
        id (int): 투표 고유 ID
        user_id (str): 사용자 식별자
        created_at (date): 투표 생성 날짜
        menu_id (int): 투표한 메뉴 ID (외래키)
        menu (Menu): 메뉴 관계 객체
    """
    __tablename__ = "votes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    created_at = Column(Date, nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.id"))
    menu = relationship("Menu", back_populates="votes", lazy="selectin")

    def __repr__(self):
        """
        객체 정보를 문자열로 반환 (디버깅용).
        """
        return f"<Vote(id={self.id}, user_id={self.user_id}, date={self.created_at}, menu={self.menu})>"
