from sqlalchemy import Column, Integer, Date
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.food_menu import food_menu_table


class Menu(Base):
    """
    Menu (메뉴) 테이블 모델.

    Attributes:
        id (int): 메뉴 고유 ID (Primary Key).
        date (date): 해당 메뉴가 제공되는 날짜.
        foods (List[Food]): 해당 메뉴에 포함된 음식 리스트 (M:N 관계).
        comments (List[Comment]): 해당 메뉴에 달린 댓글 리스트 (1:N 관계).
    """
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)

    foods = relationship("Food", secondary=food_menu_table, back_populates="menus", lazy="selectin")
    comments = relationship("Comment", back_populates="menu", lazy="selectin")

    def __repr__(self):
        """
        디버깅용 문자열 표현을 반환합니다.

        Returns:
            str: 메뉴의 ID와 날짜를 포함한 문자열 표현.
        """
        return f"<Menu(id={self.id}, date={self.date}, foods={self.foods}, comments={self.comments})>"
