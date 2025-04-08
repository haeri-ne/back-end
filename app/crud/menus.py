from datetime import date
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.sql import func
from sqlalchemy.orm import Session, joinedload

from app.models.menus import Menu
from app.schemas.menus import (
    MenuResponse, 
    MenuCreateRequest, 
    MenuCounterResponse, 
    MenuStatisticResponse
)
from app.models.foods import Food
from app.models.scores import Score
from app.models.comments import Comment
from app.models.food_menu import food_menu_table
from app.schemas.foods import FoodResponse
from app.schemas.menus import MenuCounterResponse
from app.crud.foods import get_food_statistics


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
    새로운 메뉴를 생성하고, 해당 메뉴에 포함된 음식 항목들을 연결하는 함수.

    Args:
        db (Session): SQLAlchemy 세션 객체.
        menu (MenuCreateRequest): 생성할 메뉴의 날짜와 음식 리스트.

    Returns:
        MenuResponse: 생성된 메뉴와 음식 리스트 정보.
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


def get_menu_counters(db: Session, menu_id: int) -> MenuCounterResponse:
    """
    특정 메뉴의 총 점수 개수(vote_count)와 댓글 개수(comment_count)를 반환합니다.

    Args:
        db (Session): SQLAlchemy 세션 객체.
        menu_id (int): 조회할 메뉴 ID.

    Returns:
        MenuCounterResponse: 메뉴 ID와 함께 점수/댓글 개수를 반환.
    """
    food_ids = db.query(Food.id).join(Food.menus).filter(Menu.id == menu_id).all()
    if not food_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid food_id. Food does not exist."
        )
    food_ids = [f[0] for f in food_ids]

    vote_count = (db.query(func.count(Score.id)).filter(Score.food_id.in_(food_ids)).scalar()) if food_ids else 0
    comment_count = db.query(func.count(Comment.id)).filter(Comment.menu_id == menu_id).scalar()

    return MenuCounterResponse.model_validate({
        "menu_id": menu_id,
        "vote_count": vote_count,
        "comment_count": comment_count
    })


def get_menu_statistics(db: Session, menu_id: int) -> MenuStatisticResponse:
    """
    특정 메뉴에 포함된 모든 음식들의 통계를 집계하는 함수.

    Args:
        db (Session): SQLAlchemy 세션 객체.
        menu_id (int): 조회할 메뉴 ID.

    Returns:
        MenuStatisticResponse: 각 음식별 통계와 총 평가 수를 포함한 통계 응답.
    """
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid menu_id. Menu does not exist."
        )

    total_count = 0
    foods_statistics = []

    for food in menu.foods:
        statistic = get_food_statistics(db, food.id)
        foods_statistics.append(statistic)
        total_count += statistic.count

    return MenuStatisticResponse.model_validate({
        "foods_statistics": foods_statistics,
        "total_count": total_count
    })
