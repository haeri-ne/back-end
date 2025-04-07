from typing import List, Optional
from datetime import date

from sqlalchemy.sql import func
from sqlalchemy.orm import Session, joinedload

from app.models.menus import Menu
from app.schemas.menus import MenuResponse, MenuCreateRequest
from app.models.foods import Food
from app.schemas.foods import FoodResponse
from app.models.food_menu import food_menu_table


def get_menu_by_id(db: Session, menu_id: int) -> Optional[MenuResponse]:
    """
    메뉴 ID를 통해 특정 메뉴를 조회하는 함수.

    Args:
        db (Session): 데이터베이스 세션.
        menu_id (int): 조회할 메뉴의 ID.

    Returns:
        Optional[MenuResponse]: 조회된 메뉴 정보 (없으면 None).
    """
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    
    if menu:
        return MenuResponse.model_validate(menu)
    
    return None

def get_menu_by_date(db: Session, date: date) -> List[MenuResponse]:
    """
    특정 날짜의 메뉴 목록을 조회하는 함수.

    Args:
        db (Session): 데이터베이스 세션.
        date (date): 조회할 날짜.

    Returns:
        List[MenuResponse]: 해당 날짜의 메뉴 정보.
    """
    menu_list = db.query(Menu).options(joinedload(Menu.foods)).filter(func.DATE(Menu.date) == date).all()

    return [
        MenuResponse(
            id=menu.id,
            foods=[FoodResponse(id=food.id, name=food.name) for food in menu.foods],
            date=menu.date
        )
        for menu in menu_list
    ]

def create_menu(db: Session, menu: MenuCreateRequest) -> MenuResponse:
    """
    새로운 메뉴를 생성하는 함수.

    Args:
        db (Session): 데이터베이스 세션.
        menu (MenuCreateRequest): 생성할 메뉴 정보.

    Returns:
        MenuResponse: 생성된 메뉴 정보.
    """
    new_menu = Menu(date=menu.date)
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
        date=new_menu.date
    )
