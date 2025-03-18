from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.food_menu import food_menu_table 

class Food(Base):
    """
    Food (음식) 테이블 모델.

    - `id`: 음식 고유 ID (PK)
    - `name`: 음식 이름
    - `menus`: 다대다(M:N) 관계에서 메뉴(Menu)와 연결된 리스트
    - `scores`: 음식 점수 (1:N 관계)
    """
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    menus = relationship("Menu", secondary=food_menu_table, back_populates="foods", lazy="selectin")
    scores = relationship("Score", back_populates="food", lazy="selectin")

    def __repr__(self):
        """객체 정보를 문자열로 반환 (디버깅용)."""
        return f"<Food(id={self.id}, name={self.name})>"
