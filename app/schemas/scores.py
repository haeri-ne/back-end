from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ScoreCreateRequest(BaseModel):
    """
    점수 생성 요청 모델.

    Attributes:
        score (float): 음식에 대한 평가 점수 (예: 1.0 ~ 5.0).
        food_id (int): 평가 대상 음식의 ID.
    """
    score: float
    food_id: int


class ScoreResponse(BaseModel):
    """
    점수 응답 모델.

    Attributes:
        id (int): 점수 고유 ID.
        user_id (str): 점수를 등록한 사용자 ID.
        score (float): 평가 점수.
        created_at (datetime): 점수 등록 시간.
        food_id (int): 평가 대상 음식 ID.
    """
    id: int
    user_id: str
    score: float
    created_at: datetime
    food_id: int

    model_config = ConfigDict(from_attributes=True)
