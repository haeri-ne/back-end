from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_admin
from app.dependencies.user import get_user_id
from app.crud import foods
from app.models.users import User
from app.schemas.foods import FoodPatchRequest, FoodResponse, FoodStatisticResponse
from app.schemas.scores import ScoreCreateRequest, ScoreResponse


router = APIRouter(
    prefix="/foods",
    tags=["foods"],
    responses={404: {"description": "Not found"}},
)


@router.patch("/{food_id}", response_model=FoodResponse, status_code=status.HTTP_200_OK)
async def update_food(
    food_id: int,
    new_food: FoodPatchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    음식 정보를 수정하는 API (관리자 권한 필요).

    Args:
        food_id (int): 수정할 음식의 ID.
        new_food (FoodPatchRequest): 변경할 음식 이름 등의 정보.
        db (Session): SQLAlchemy 데이터베이스 세션.
        current_user (User): 현재 요청한 관리자 사용자 (의존성 주입).

    Returns:
        FoodResponse: 수정된 음식 정보.

    Raises:
        HTTPException: 음식 ID가 존재하지 않거나, 권한이 없을 경우.
    """
    updated_food = foods.update_food(db, food_id, new_food)
    return updated_food


@router.post("/score", response_model=List[ScoreResponse], status_code=status.HTTP_201_CREATED)
async def score_food(
    score_list: List[ScoreCreateRequest],
    db: Session = Depends(get_db),
    user_id: str = Depends(get_user_id)
):
    """
    음식에 대한 점수를 등록하는 API.

    사용자로부터 음식 ID와 점수 리스트를 받아 각 점수를 저장합니다.

    Args:
        score_list (List[ScoreCreateRequest]): 점수 생성 요청 리스트.
        db (Session): SQLAlchemy 데이터베이스 세션.
        user_id (str): 요청자의 사용자 ID (헤더에서 추출).

    Returns:
        List[ScoreResponse]: 생성된 점수 정보 리스트.

    Raises:
        HTTPException: 유효하지 않은 food_id 또는 DB 오류 발생 시 예외.
    """
    new_score = foods.score_food(db, user_id, score_list)
    return new_score


@router.get("/{food_id}/statistic", response_model=FoodStatisticResponse, status_code=status.HTTP_200_OK)
async def get_food_statistics(
    food_id: int,
    db: Session = Depends(get_db)
):
    """
    특정 음식의 점수 통계를 조회하는 API.

    Args:
        food_id (int): 조회할 음식의 ID.
        db (Session): SQLAlchemy 데이터베이스 세션.

    Returns:
        FoodStatisticResponse: 평균, 중앙값, 분위수 등 점수 통계 정보.

    Raises:
        HTTPException: 음식이 존재하지 않거나 점수가 없을 경우.
    """
    statistics = foods.get_food_statistics(db, food_id)
    return statistics
