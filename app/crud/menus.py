from typing import List, Optional
from datetime import datetime, date

from sqlalchemy.sql import func
from sqlalchemy.orm import Session, joinedload

from app.models.menus import Menu
from app.schemas.menus import MenuResponse, MenuCreateRequest
from app.models.foods import Food
from app.schemas.foods import FoodResponse


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

def get_menu_by_date(db: Session, date: date) -> List[Menu]:
    """
    특정 날짜의 메뉴 목록을 조회하는 함수.

    Args:
        db (Session): 데이터베이스 세션.
        date (date): 조회할 날짜.

    Returns:
        List[Menu]: 해당 날짜의 메뉴 목록.
    """
    return db.query(Menu).options(joinedload(Menu.foods)).filter(func.DATE(Menu.date) == date).all()

def create_menu(db: Session, menu: MenuCreateRequest) -> MenuResponse:
    """
    새로운 메뉴를 생성하는 함수.

    Args:
        db (Session): 데이터베이스 세션.
        menu (MenuCreateRequest): 생성할 메뉴 정보.

    Returns:
        MenuResponse: 생성된 메뉴 정보.
    """
    new_menu = Menu(
        date=datetime.now()
    )
    db.add(new_menu)
    db.flush()
    db.refresh(new_menu)

    created_foods = []
    for food in menu.foods:
        new_food = Food(name=food, menu_id=new_menu.id)
        db.add(new_food)
        db.flush()
        created_foods.append(FoodResponse(id=new_food.id, name=new_food.name))

    return MenuResponse(
        foods=created_foods,
        date=new_menu.date
    )
