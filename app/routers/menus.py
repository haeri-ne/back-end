from typing import List
from datetime import date

from sqlalchemy.orm import Session

from fastapi import APIRouter, HTTPException, Depends, Path, status
from fastapi_pagination import add_pagination

from app.database import get_db
from app.dependencies.auth import get_current_admin
from app.dependencies.user import get_user_id
from app.crud import menus
from app.crud import comments
from app.models.users import User
from app.schemas.menus import (
    MenuResponse, 
    MenuCreateRequest, 
    MenuCounterResponse, 
    MenuStatisticResponse
)
from app.schemas.comments import CommentRequest, CommentResponse


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


@router.post("/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment: CommentRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_user_id)
):
    """
    메뉴에 대한 댓글을 작성하는 API.

    Args:
        comment (CommentRequest): 작성할 댓글 정보.
        db (Session): SQLAlchemy 세션 객체.
        user_id (str): 요청자 사용자 ID (헤더에서 추출).

    Returns:
        CommentResponse: 생성된 댓글 정보.

    Raises:
        HTTPException: 댓글 저장에 실패할 경우 500 예외 발생.
    """
    new_comment = comments.create_comment(db, user_id, comment)

    if not new_comment:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create comment"
        )

    return new_comment


@router.get("/{menu_id}/counters", response_model=MenuCounterResponse, status_code=status.HTTP_200_OK)
async def get_menu_counters(menu_id: int, db: Session = Depends(get_db)):
    """
    특정 메뉴의 점수 개수(vote_count)와 댓글 개수(comment_count)를 조회하는 API.

    Args:
        menu_id (int): 조회할 메뉴의 ID.
        db (Session): SQLAlchemy 데이터베이스 세션.

    Returns:
        MenuCounterResponse: 해당 메뉴에 연결된 음식들의 점수 수와 댓글 수.
    
    Raises:
        HTTPException: 메뉴에 연결된 음식이 하나도 없는 경우 400 예외 반환.
    """
    counters = menus.get_menu_counters(db, menu_id)
    return counters


@router.get("/{menu_id}/statistics", response_model=MenuStatisticResponse, status_code=status.HTTP_200_OK)
async def get_menu_statistics(
    menu_id: int,
    db: Session = Depends(get_db)
):
    """
    특정 메뉴에 포함된 음식들에 대한 점수 통계를 조회하는 API.

    Args:
        menu_id (int): 조회할 메뉴의 ID.
        db (Session): SQLAlchemy 세션 객체.

    Returns:
        MenuStatisticResponse: 메뉴에 포함된 음식들의 점수 통계.

    Raises:
        HTTPException: 메뉴가 존재하지 않을 경우 400 예외 발생.
    """
    statistics = menus.get_menu_statistics(db, menu_id)
    return statistics
