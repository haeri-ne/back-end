from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud import statistics
from app.schemas.statistics import (
    MenuStatisticResponse, 
    MenuMeanStatisticResponse,
    FoodStatisticResponse,
    FoodMeanStatisticResponse
)

router = APIRouter(
    prefix="/statistics", 
    tags=["statistics"],
    responses={404: {"description": "Not found"}}
)


@router.get("/menus/{menu_id}", response_model=MenuStatisticResponse, status_code=status.HTTP_200_OK)
async def get_menu_statistics(
    menu_id: int,
    date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    특정 메뉴에 포함된 음식들의 통계 정보를 조회합니다.

    Args:
        menu_id (int): 통계를 조회할 메뉴의 ID.
        date (Optional[datetime], optional): 특정 날짜 기준 통계 조회. 기본값은 None.
        db (Session): 데이터베이스 세션 (의존성 주입).

    Returns:
        MenuStatisticResponse: 각 음식에 대한 상세 통계 정보와 전체 평가 수.

    Raises:
        HTTPException: 메뉴가 존재하지 않거나 통계 데이터를 찾을 수 없는 경우.
    """
    statistic = statistics.get_menu_statistics(db, menu_id, date)
    return statistic


@router.get("/mean/menus/{menu_id}", response_model=MenuMeanStatisticResponse, status_code=status.HTTP_200_OK)
async def get_menu_mean(
    menu_id: int,
    date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    특정 메뉴에 포함된 음식들의 평균 점수를 조회합니다.

    Args:
        menu_id (int): 평균 점수를 조회할 메뉴의 ID.
        date (Optional[datetime], optional): 특정 날짜 기준 평균 조회. 기본값은 None.
        db (Session): 데이터베이스 세션 (의존성 주입).

    Returns:
        MenuMeanStatisticResponse: 각 음식에 대한 평균 점수 리스트와 통계 생성일.
    """
    statistic = statistics.get_menu_mean(db, menu_id, date)
    return statistic


@router.get("/foods/{food_id}", response_model=FoodStatisticResponse, status_code=status.HTTP_200_OK)
async def get_food_statistics(
    food_id: int,
    db: Session = Depends(get_db)
):
    """
    특정 음식의 점수 통계를 조회합니다.

    Args:
        food_id (int): 통계를 조회할 음식의 ID.
        db (Session): 데이터베이스 세션 (의존성 주입).

    Returns:
        FoodStatisticResponse: 평균, 중앙값, 분위수, 최소/최대값 등의 통계 정보.

    Raises:
        HTTPException: 음식이 존재하지 않거나 평가 데이터가 없는 경우.
    """
    statistic = statistics.get_food_statistics(db, food_id)
    return statistic


@router.get("/mean/foods/{food_id}", response_model=FoodMeanStatisticResponse, status_code=status.HTTP_200_OK)
async def get_food_mean(
    food_id: int,
    date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    특정 음식의 평균 점수를 조회합니다.

    Args:
        food_id (int): 평균 점수를 조회할 음식의 ID.
        date (Optional[datetime], optional): 특정 날짜 기준 평균 조회. 기본값은 None.
        db (Session): 데이터베이스 세션 (의존성 주입).

    Returns:
        FoodMeanStatisticResponse: 해당 음식의 평균 점수.

    Raises:
        HTTPException: 음식이 존재하지 않거나 평가 데이터가 없는 경우.
    """
    statistic = statistics.get_food_mean(db, food_id, date)
    return statistic
