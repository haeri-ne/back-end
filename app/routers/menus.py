from typing import List
from datetime import date

from sqlalchemy.orm import Session

from fastapi import APIRouter, HTTPException, Depends, Path, status
from fastapi_pagination import add_pagination

from app.database import get_db
from app.dependencies.auth import get_current_admin
from app.crud import menus
from app.models.users import User
from app.schemas.menus import (
    MenuResponse, 
    MenuCreateRequest
)


router = APIRouter(
    prefix="/menus",
    tags=["menus"],
    responses={404: {"description": "Not found"}},
)
add_pagination(router)


@router.get("/{date}", response_model=List[MenuResponse])
async def get_menu_by_date(
    date: date = Path(..., description="조회할 날짜 (YYYY-MM-DD 형식)"),
    db: Session = Depends(get_db),
):
    """
    특정 날짜의 메뉴 목록을 조회하는 API.

    Args:
        date (date): 조회할 날짜 (`YYYY-MM-DD` 형식).
        db (Session): SQLAlchemy 세션 객체.

    Returns:
        List[MenuResponse]: 해당 날짜에 존재하는 메뉴 목록.

    Raises:
        HTTPException: 메뉴가 존재하지 않을 경우 404 예외 발생.
    """
    menu_list = menus.get_menu_by_date(db, date)

    if not menu_list:
        raise HTTPException(
            status_code=404, 
            detail="No menus found for the given date."
        )

    return menu_list


@router.post("/", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
async def create_menu(
    menu: MenuCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    새로운 메뉴를 생성하는 API (관리자 권한 필요).

    Args:
        menu (MenuCreateRequest): 생성할 메뉴 정보.
        db (Session): SQLAlchemy 세션 객체.
        current_user (User): 관리자 권한이 있는 사용자 객체.

    Returns:
        MenuResponse: 생성된 메뉴 정보.

    Raises:
        HTTPException: 메뉴 생성에 실패할 경우 500 예외 발생.
    """
    new_menu = menus.create_menu(db, menu)

    if not new_menu:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create menu."
        )

    return new_menu
