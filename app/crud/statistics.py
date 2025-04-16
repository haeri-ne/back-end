from collections import defaultdict
from datetime import datetime
import numpy as np

from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.models.menus import Menu
from app.models.foods import Food
from app.models.scores import Score
from app.schemas.statistics import (
    MenuStatisticResponse, 
    MenuMeanStatisticResponse,
    FoodStatisticResponse, 
    FoodMeanStatisticResponse,
    FoodStatisticsIncludingDuplicate,
    FoodStatisticsWithoutDuplicate
)


def get_menu_mean(db: Session, menu_id: int, date: datetime=None) -> MenuMeanStatisticResponse:
    """
    특정 메뉴에 포함된 음식들의 평균 점수를 조회합니다.

    Args:
        db (Session): SQLAlchemy 세션 객체.
        menu_id (int): 메뉴 ID.
        date (datetime, optional): 특정 날짜 기준 조회. 기본값은 전체.

    Returns:
        MenuMeanStatisticResponse: 메뉴에 속한 음식들의 평균 점수 목록과 생성 날짜.

    Raises:
        HTTPException: 메뉴가 존재하지 않을 경우 400 예외 발생.
    """
    menu = db.query(Menu).filter(Menu.id == menu_id).first() 
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid menu_id. Menu does not exist."
        )
    
    foods_statistics = []
    for food in menu.foods:
        statistic = get_food_mean(db, food.id, date)
        foods_statistics.append(statistic)
    
    return MenuMeanStatisticResponse.model_validate({
        "menu_id": menu_id,
        "foods_statistics": foods_statistics,
        "date": date
    })


def get_menu_statistics(db: Session, menu_id: int, date: datetime=None) -> MenuStatisticResponse:
    """
    특정 메뉴에 포함된 음식들의 통계 정보를 조회합니다.

    Args:
        db (Session): SQLAlchemy 세션 객체.
        menu_id (int): 메뉴 ID.
        date (datetime, optional): 특정 날짜 기준 조회. 기본값은 전체.

    Returns:
        MenuStatisticResponse: 각 음식별 통계와 총 평가 수, 평균 점수를 포함한 결과.

    Raises:
        HTTPException: 메뉴가 존재하지 않을 경우 400 예외 발생.
    """
    menu = db.query(Menu).filter(Menu.id == menu_id).first() 
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid menu_id. Menu does not exist."
        )

    total_count_including_duplicates = total_count_without_duplicates = 0
    total_sum_including_duplicates = total_sum_without_duplicates = 0
    foods_statistics = []

    for food in menu.foods:
        statistic = get_food_statistics(db, food.id, date)
        foods_statistics.append(statistic)
        total_count_including_duplicates += statistic.statistics_including_duplicates.total
        total_sum_including_duplicates += statistic.statistics_including_duplicates.mean
        total_count_without_duplicates += statistic.statistics_without_duplicates.total
        total_sum_without_duplicates += statistic.statistics_without_duplicates.mean

    return MenuStatisticResponse.model_validate({
        "foods_statistics": foods_statistics,
        "total_count_including_duplicates": total_count_including_duplicates,
        "total_count_without_duplicates": total_count_without_duplicates,
        "total_avg_including_duplicates": total_sum_including_duplicates / len(statistic.statistics_including_duplicates.scores),
        "total_avg_without_duplicates": total_sum_without_duplicates / len(statistic.statistics_without_duplicates.scores)
    })


def get_food_mean(db: Session, food_id: int, date: datetime=None) -> FoodMeanStatisticResponse:
    """
    특정 음식의 평균 점수를 계산합니다.

    Args:
        db (Session): SQLAlchemy 세션 객체.
        food_id (int): 음식 ID.
        date (datetime, optional): 특정 날짜 기준 조회. 기본값은 전체.

    Returns:
        FoodMeanStatisticResponse: 음식 ID와 평균 점수.

    Raises:
        HTTPException: 음식이 존재하지 않을 경우 404 예외 발생.
    """
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid food_id. Food does not exist."
        )
    
    arr = np.array([score for _, score in _get_scores_without_duplicates(db, food, date)])
    
    return FoodMeanStatisticResponse.model_validate({
        "food_id": food.id,
        "mean": float(np.mean(arr)),
    })


def get_food_statistics(db: Session, food_id: int, date: datetime=None) -> FoodStatisticResponse:
    """
    특정 음식에 대한 평가 통계를 계산합니다.

    Args:
        db (Session): SQLAlchemy 세션 객체.
        food_id (int): 음식 ID.
        date (datetime, optional): 특정 날짜 기준 조회. 기본값은 전체.

    Returns:
        FoodStatisticResponse: 평균, 중앙값, 분위수, 최소/최대 등 포함된 통계 정보.

    Raises:
        HTTPException: 음식이 존재하지 않거나 평가 점수가 없을 경우.
    """
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid food_id. Food does not exist."
        )
    
    scores_including_duplicates_list = []
    scores_including_duplicates_dict = defaultdict(list)
    for user_id, score in _get_scores_including_duplicates(db, food, date):
        scores_including_duplicates_dict[user_id].append(score)
        scores_including_duplicates_list.append(score)

    scores_without_duplicates_list = []
    scores_without_duplicates_dict = defaultdict(float)
    for user_id, score in _get_scores_without_duplicates(db, food, date):
        scores_without_duplicates_dict[user_id] = score
        scores_without_duplicates_list.append(score)

    arr_including_duplicates = np.array(scores_including_duplicates_list)
    arr_without_duplicates = np.array(scores_without_duplicates_list)
    
    return FoodStatisticResponse.model_validate({
        "food_id": food_id,
        "statistics_including_duplicates": FoodStatisticsIncludingDuplicate.model_validate({
            "scores": scores_including_duplicates_dict,
            "total": len(arr_including_duplicates),
            "mean": float(np.mean(arr_including_duplicates)),
            "median": float(np.median(arr_including_duplicates)),
            "quantile_25": float(np.percentile(arr_including_duplicates, 25)),
            "quantile_75": float(np.percentile(arr_including_duplicates, 75)),
            "min": float(np.min(arr_including_duplicates)),
            "max": float(np.max(arr_including_duplicates))
        }),
        "statistics_without_duplicates": FoodStatisticsWithoutDuplicate.model_validate({
            "scores": scores_without_duplicates_dict,
            "total": len(arr_without_duplicates),
            "mean": float(np.mean(arr_without_duplicates)),
            "median": float(np.median(arr_without_duplicates)),
            "quantile_25": float(np.percentile(arr_without_duplicates, 25)),
            "quantile_75": float(np.percentile(arr_without_duplicates, 75)),
            "min": float(np.min(arr_without_duplicates)),
            "max": float(np.max(arr_without_duplicates))
        })
    })


def _get_scores_including_duplicates(db: Session, food: Food, date: datetime=None):
    """
    중복 포함 점수 목록을 조회합니다.

    Args:
        db (Session): SQLAlchemy 세션.
        food (Food): 조회할 음식 객체.
        date (datetime, optional): 특정 날짜 기준 조회.

    Returns:
        List[Tuple[int, float]]: (user_id, score)의 리스트.
    """
    if date:
        return (
            db
            .query(Score.user_id, Score.score)
            .filter(and_(Score.food_id == food.id), func.DATE(Score.created_at) == func.DATE(date))
            .all()
        )
    else:
        return (
            db
            .query(Score.user_id, Score.score)
            .filter(Score.food_id == food.id)
            .all()
        )


def _get_scores_without_duplicates(db: Session, food: Food, date: datetime=None):
    """
    사용자별로 평균을 계산하여 중복 제거된 점수 목록을 조회합니다.

    Args:
        db (Session): SQLAlchemy 세션.
        food (Food): 조회할 음식 객체.
        date (datetime, optional): 특정 날짜 기준 조회.

    Returns:
        List[Tuple[int, float]]: (user_id, 평균 점수)의 리스트.
    """
    if date:
        return (
            db
            .query(Score.user_id, func.avg(Score.score))
            .filter(and_(Score.food_id == food.id, func.DATE(Score.created_at) == func.DATE(date)))
            .group_by(Score.user_id)
            .all()
        )
    else:
        return (
            db
            .query(Score.user_id, func.avg(Score.score))
            .filter(Score.food_id == food.id)
            .group_by(Score.user_id)
            .all()
        )
