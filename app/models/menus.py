from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.food_menu import food_menu_table


class Menu(Base):
    """
    Menu (메뉴) 테이블 모델.

    Attributes:
        id (Integer): 메뉴 고유 ID (Primary Key)
        created_at (DateTime): 해당 메뉴가 제공되는 일자
        foods (List[Food]): 해당 메뉴의 음식 리스트 (M:N 관계)
        comments (List[Comment]): 해당 메뉴의 댓글 리스트 (1:N 관계)
        votes (List[Vote]): 해당 메뉴의 투표 리스트 (1:N 관계)
    """
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False)

    foods = relationship("Food", secondary=food_menu_table, back_populates="menus", lazy="selectin")
    comments = relationship("Comment", back_populates="menu", lazy="selectin")
    votes = relationship("Vote", back_populates="menu", lazy="selectin")

    def __repr__(self):
        """객체 정보를 문자열로 반환 (디버깅용)."""
        return f"<Menu(id={self.id}, date={self.date}, foods={self.foods}, comments={self.comments})>"
