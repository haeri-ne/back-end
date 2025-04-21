from datetime import datetime
from typing import List

from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from app.models.scores import Score
from app.schemas.scores import ScoreCreateRequest, ScoreResponse
from app.models.foods import Food
from app.models.menus import Menu


def create_food_scores(db: Session, user_id: str, score_list: List[ScoreCreateRequest]) -> List[ScoreResponse]:
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


def get_recent_food_scores_by_menu(db: Session, user_id: str, menu_id: int) -> List[ScoreResponse]:
    """
    특정 메뉴에 포함된 음식들에 대해 사용자가 가장 최근에 등록한 점수를 조회합니다.

    Args:
        db (Session): SQLAlchemy 세션.
        user_id (str): 사용자 식별자.
        menu_id (int): 조회 대상 메뉴 ID.

    Returns:
        List[ScoreResponse]: 음식별 최근 점수 목록.

    Raises:
        HTTPException:
            - 메뉴가 존재하지 않을 경우 400 에러.
            - 유저가 남긴 점수가 전혀 없을 경우 400 에러.
    """
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid menu_id. Menu does not exist."
        )
    
    scores = [
        score for food in menu.foods
        if (score := db.query(Score)
            .filter(and_(Score.user_id == user_id, Score.food_id == food.id))
            .order_by(Score.id.desc())
            .first())
    ]
    
    if not scores:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No scores found for this menu."
        )
    
    return [ScoreResponse.model_validate(score) for score in scores]
