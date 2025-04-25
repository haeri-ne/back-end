from datetime import date
from typing import List, Optional

from sqlalchemy.sql import func
from sqlalchemy.orm import Session, joinedload

from app.models.menus import Menu
from app.schemas.menus import (
    MenuResponse, 
    MenuCreateRequest
)
from app.models.foods import Food
from app.models.food_menu import food_menu_table
from app.schemas.foods import FoodResponse


def get_menu_by_id(db: Session, menu_id: int) -> Optional[MenuResponse]:
    """
    메뉴 ID를 통해 특정 메뉴를 조회하는 함수.

    Args:
        db (Session): SQLAlchemy 세션 객체.
        menu_id (int): 조회할 메뉴의 ID.

    Returns:
        Optional[MenuResponse]: 해당 ID의 메뉴가 존재하면 MenuResponse, 없으면 None 반환.
    """
    menu = db.query(Menu).filter(Menu.id == menu_id).first()

    if menu:
        return MenuResponse.model_validate(menu)

    return None


def get_menu_by_date(db: Session, date: date) -> List[MenuResponse]:
    """
    특정 날짜에 해당하는 모든 메뉴 목록을 조회하는 함수.

    Args:
        db (Session): SQLAlchemy 세션 객체.
        date (date): 조회할 날짜.

    Returns:
        List[MenuResponse]: 해당 날짜에 존재하는 모든 메뉴 리스트.
    """
    menu_list = db.query(Menu).options(joinedload(Menu.foods)).filter(func.DATE(Menu.created_at) == date).all()

    return [
        MenuResponse(
            id=menu.id,
            foods=[FoodResponse(id=food.id, name=food.name) for food in menu.foods],
            date=menu.created_at
        )
        for menu in menu_list
    ]


def create_menu(db: Session, menu: MenuCreateRequest) -> MenuResponse:
    """
    새로운 메뉴를 생성하고, 해당 메뉴에 포함된 음식 항목들을 연결하는 함수.

    Args:
        db (Session): SQLAlchemy 세션 객체.
        menu (MenuCreateRequest): 생성할 메뉴의 날짜와 음식 리스트.

    Returns:
        MenuResponse: 생성된 메뉴와 음식 리스트 정보.
    """
    new_menu = Menu(created_at=menu.date)
    db.add(new_menu)
    db.flush()
    db.refresh(new_menu)

    created_foods = []
    for food in menu.foods:
        existing_food = db.query(Food).filter(Food.name == food).first()

        if existing_food:
            new_food = existing_food
        else:
            new_food = Food(name=food)
            db.add(new_food)
            db.flush()

        db.execute(food_menu_table.insert().values(food_id=new_food.id, menu_id=new_menu.id))
        created_foods.append(FoodResponse(id=new_food.id, name=new_food.name))

    return MenuResponse(
        id=new_menu.id,
        foods=created_foods,
        date=new_menu.created_at
    )
