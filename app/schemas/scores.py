from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ScoreCreateRequest(BaseModel):
    """점수 생성 요청"""
    score: float
    food_id: int

class ScoreResponse(BaseModel):
    """점수 응답 모델"""
    id: int
    score: float
    created_at: datetime
    food_id: int

    model_config = ConfigDict(from_attributes=True)
