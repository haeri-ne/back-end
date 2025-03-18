from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.database import get_db
from app.crud import foods
from app.schemas.scores import ScoreCreateRequest, ScoreResponse


router = APIRouter(
    prefix="/foods",
    tags=["foods"],
    responses={404: {"description": "Not found"}},
)


@router.post("/score", response_model=ScoreResponse, status_code=status.HTTP_201_CREATED)
async def score_food(
    score: ScoreCreateRequest,
    db: Session = Depends(get_db)
):
    """
    음식 점수를 저장하는 API.

    음식의 ID(`food_id`)와 점수(`score`)를 받아 새로운 점수를 생성합니다.
    생성된 점수는 데이터베이스에 저장되며, `201 Created` 응답과 함께 반환됩니다.

    Args:
        score (ScoreCreateRequest): 음식 ID 및 점수를 포함하는 요청 데이터.
        db (Session): 데이터베이스 세션.

    Returns:
        ScoreResponse: 생성된 점수 정보를 포함한 `201 Created` 응답.
    
    Raises:
        HTTPException: 요청 데이터가 유효하지 않거나, DB 저장 중 오류가 발생할 경우 예외 발생.
    """
    new_score = foods.score_food(db, score)
    
    return new_score
