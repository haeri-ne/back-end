from typing import List
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.foods import FoodResponse

class MenuCreateRequest(BaseModel):
    """메뉴 생성 요청"""
    foods: List[str]
    date: datetime

class MenuResponse(BaseModel):
    """메뉴 응답 모델"""
    id: int
    foods: List[FoodResponse]
    date: datetime

    model_config = ConfigDict(from_attributes=True)
