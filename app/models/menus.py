from sqlalchemy import Column, Integer, Date
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.food_menu import food_menu_table  

class Menu(Base):
    """
    Menu (메뉴) 테이블 모델.

    - `id`: 메뉴 고유 ID (PK)
    - `date`: 해당 메뉴의 날짜
    - `foods`: 다대다(M:N) 관계에서 음식(Food)과 연결된 리스트
    """
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)

    foods = relationship("Food", secondary=food_menu_table, back_populates="menus", lazy="selectin")

    def __repr__(self):
        """객체 정보를 문자열로 반환 (디버깅용)."""
        return f"<Menu(id={self.id}, date={self.date})>"
