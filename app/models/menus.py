from sqlalchemy import Column, Integer, Date
from sqlalchemy.orm import relationship

from app.database import Base

class Menu(Base):
    """
    메뉴 모델.

    날짜(`date`)를 기준으로 여러 개의 `Food` 객체와 연결됨 (1:N 관계).
    """
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)

    foods = relationship("Food", back_populates="menu", lazy="selectin")  

    def __repr__(self):
        """객체 정보를 문자열로 반환 (디버깅용)."""
        return f"<Menu(id={self.id}, date={self.date})>"
