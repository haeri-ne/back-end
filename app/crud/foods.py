from datetime import datetime

from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from app.models.scores import Score
from app.schemas.scores import ScoreCreateRequest, ScoreResponse
from app.models.foods import Food
from app.schemas.foods import FoodCreateRequest, FoodResponse

def create_food(db: Session, food: FoodCreateRequest) -> FoodResponse:
    """
    새로운 음식을 생성하는 함수.

    Args:
        db (Session): 데이터베이스 세션.
        food (FoodCreateRequest): 생성할 음식 정보.

    Returns:
        FoodResponse: 생성된 음식 정보.
    
    Raises:
        HTTPException: 메뉴 ID(`menu_id`)가 존재하지 않을 경우 예외 발생.
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


def score_food(db: Session, score: ScoreCreateRequest) -> ScoreResponse:
    """
    특정 음식에 대한 점수를 저장하는 함수.

    Args:
        db (Session): 데이터베이스 세션.
        score (ScoreCreateRequest): 음식 ID 및 점수 정보.

    Returns:
        ScoreResponse: 저장된 점수 정보.

    Raises:
        HTTPException: 음식 ID(`food_id`)가 존재하지 않을 경우 예외 발생.
    """
    food = db.query(Food).filter(Food.id == score.food_id).first()
    if not food:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid food_id. Food does not exist."
        )

    new_score = Score(
        food_id=score.food_id,
        score=score.score,
        created_at=datetime.now()
    )
    db.add(new_score)
    db.flush()

    return ScoreResponse.model_validate(new_score)
