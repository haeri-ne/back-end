"""
food_menu.py - 메뉴(Food)와 음식(Menu) 간 다대다(M:N) 관계를 위한 중간 테이블 정의.
"""

from sqlalchemy import Table, Column, ForeignKey
from app.database import Base

food_menu_table = Table(
    "food_menu_table",
    Base.metadata,
    Column("food_id", ForeignKey("foods.id"), primary_key=True),
    Column("menu_id", ForeignKey("menus.id"), primary_key=True) 
)
