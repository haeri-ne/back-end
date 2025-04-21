from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Vote(Base):
    """
    투표(Vote) 테이블 모델.

    Attributes:
        id (Integer): 투표 고유 ID (Primary Key)
        user_id (String(100)): 사용자 식별자 (UUID)
        created_at (DateTime): 투표 일자
        menu_id (Integer): 투표한 메뉴 ID (Foreign Key)
        menu (Menu): 투표한 메뉴 객체 (1:N 관계)
    """
    __tablename__ = "votes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    menu_id = Column(Integer, ForeignKey("menus.id"))
    menu = relationship("Menu", back_populates="votes", lazy="selectin")

    def __repr__(self):
        """객체 정보를 문자열로 반환 (디버깅용)."""
        return f"<Vote(id={self.id}, user_id={self.user_id}, menu={self.menu}, created_at={self.created_at})>"
