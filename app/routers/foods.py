from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_admin
from app.crud import foods
from app.models.users import User
from app.schemas.foods import FoodPatchRequest, FoodResponse


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
