from datetime import datetime
from typing import List

import numpy as np

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.scores import Score
from app.schemas.scores import ScoreCreateRequest, ScoreResponse
from app.models.foods import Food
from app.schemas.foods import FoodCreateRequest, FoodPatchRequest, FoodResponse, FoodStatisticResponse


def create_food(db: Session, food: FoodCreateRequest) -> FoodResponse:
    """
    새로운 음식을 생성하는 함수.

    Args:
        db (Session): SQLAlchemy 세션 객체.
        food (FoodCreateRequest): 생성할 음식의 이름과 메뉴 ID.

    Returns:
        FoodResponse: 생성된 음식의 정보.

    Raises:
        HTTPException: 주어진 menu_id가 존재하지 않을 경우 400 예외 발생.
    """
    if not db.query(Food).filter(Food.menu_id == food.menu_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid menu_id. Menu does not exist."
        )

    new_food = Food(
        name=food.name,
        menu_id=food.menu_id
    )
    db.add(new_food)
    db.flush()

    return FoodResponse.model_validate(new_food)


def update_food(db: Session, food_id: int, new_food: FoodPatchRequest) -> FoodResponse:
    """
    특정 음식의 이름을 수정하는 함수.

    Args:
        db (Session): SQLAlchemy 세션 객체.
        food_id (int): 수정할 음식의 ID.
        new_food (FoodPatchRequest): 수정할 음식 이름.

    Returns:
        FoodResponse: 수정된 음식 정보.

    Raises:
        HTTPException: food_id에 해당하는 음식이 존재하지 않을 경우 404 예외 발생.
    """
    food = db.query(Food).filter(Food.id == food_id).first()

    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food with id {food_id} not found."
        )

    food.name = new_food.updated_name

    db.commit()
    db.refresh(food)

    return FoodResponse.model_validate(food)


def score_food(db: Session, user_id: str, score_list: List[ScoreCreateRequest]) -> List[ScoreResponse]:
    """
    음식에 대한 평가 점수를 저장하는 함수.

    Args:
        db (Session): SQLAlchemy 세션 객체.
        user_id (str): 점수를 등록한 사용자 ID.
        score_list (List[ScoreCreateRequest]): 음식 ID 및 점수 목록.

    Returns:
        List[ScoreResponse]: 저장된 점수 정보 리스트.

    Raises:
        HTTPException: 음식 ID가 존재하지 않을 경우 400 예외 발생.
    """
    new_scores = []

    for score in score_list:
        food = db.query(Food).filter(Food.id == score.food_id).first()

        if not food:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid food_id. Food does not exist."
            )

        new_score = Score(
            user_id=user_id,
            food_id=score.food_id,
            score=score.score,
            created_at=datetime.now()
        )

        new_scores.append(new_score)
        db.add(new_score)
        db.flush()

    return [ScoreResponse.model_validate(new_score) for new_score in new_scores]


def get_food_statistics(db: Session, food_id: int) -> FoodStatisticResponse:
    """
    특정 음식에 대한 평가 점수 통계를 계산하는 함수.

    Args:
        db (Session): SQLAlchemy 세션 객체.
        food_id (int): 통계를 계산할 음식 ID.

    Returns:
        FoodStatisticResponse: 평균, 중앙값, 분위수, 최소/최대 점수 등을 포함한 통계 결과.

    Raises:
        HTTPException: 음식이 존재하지 않거나 점수가 없을 경우 404 예외 발생.
    """
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid food_id. Food does not exist."
        )

    scores = db.query(Score.score).filter(Score.food_id == food.id).all()
    scores_list = [s[0] for s in scores]

    if not scores_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No scores found for this food."
        )

    arr = np.array(scores_list)

    return FoodStatisticResponse.model_validate({
        "food_id": food_id,
        "count": len(arr),
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "quantile_25": float(np.percentile(arr, 25)),
        "quantile_75": float(np.percentile(arr, 75)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr))
    })
