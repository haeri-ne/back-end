from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.user import get_user_id
from app.crud import scores
from app.schemas.scores import ScoreCreateRequest, ScoreResponse


router = APIRouter(
    prefix="/scores", 
    tags=["scores"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=List[ScoreResponse], status_code=status.HTTP_201_CREATED)
async def create_food_scores(
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
    new_score = scores.create_food_scores(db, user_id, score_list)
    return new_score


@router.get("/{menu_id}", response_model=List[ScoreResponse], status_code=status.HTTP_200_OK)
async def get_recent_food_scores_by_menu(
    menu_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_user_id)
):
    """
    특정 메뉴에 포함된 음식들에 대해 사용자가 가장 최근에 남긴 점수들을 조회합니다.

    - 사용자는 각 음식마다 여러 개의 점수를 남길 수 있지만, 이 API는 **가장 최근 점수 1개씩만 반환**합니다.
    - 메뉴에 포함된 음식 중, 사용자가 점수를 남기지 않은 음식은 응답에서 제외됩니다.

    Args:
        menu_id (int): 점수를 조회할 대상 메뉴 ID.
        db (Session): SQLAlchemy 세션 객체.
        user_id (str): 사용자 식별자 (헤더에서 추출됨).

    Returns:
        List[ScoreResponse]: 음식별 최근 점수 목록.

    Raises:
        HTTPException:
            - 존재하지 않는 메뉴 ID일 경우 400 에러.
            - 사용자가 해당 메뉴에 속한 음식에 대해 점수를 남기지 않았을 경우 400 에러.
    """
    score = scores.get_recent_food_scores_by_menu(db, user_id, menu_id)
    return score
