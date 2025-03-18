from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class Food(Base):
    """
    음식(Food) 모델.

    특정 메뉴(`menu_id`)에 속하며, 여러 개의 점수(`scores`)와 연결됨.
    """
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)

    menu = relationship("Menu", back_populates="foods", lazy="selectin")

    scores = relationship("Score", back_populates="food", lazy="selectin")  

    def __repr__(self):
        """객체 정보를 문자열로 반환 (디버깅용)."""
        return f"<Food(id={self.id}, name={self.name}, menu_id={self.menu_id})>"
