from sqlalchemy import Table, Column, ForeignKey
from app.database import Base

"""
Menu(음식)와 Food(음식) 간 다대다(M:N) 관계를 위한 중간 테이블.

Attributes:
    food_id: 음식 ID.
    menu_id: 메뉴 ID.
"""
food_menu_table = Table(
    "food_menu_table",
    Base.metadata,
    Column("food_id", ForeignKey("foods.id"), primary_key=True, index=True),
    Column("menu_id", ForeignKey("menus.id"), primary_key=True, index=True) 
)
