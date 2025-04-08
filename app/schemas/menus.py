from typing import List
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.schemas.foods import FoodResponse, FoodStatisticResponse


class MenuCreateRequest(BaseModel):
    """
    메뉴 생성 요청 모델.

    Attributes:
        foods (List[str]): 생성할 음식 이름 리스트.
        date (datetime): 메뉴 날짜 (YYYY-MM-DD 형식 권장).
    """
    foods: List[str]
    date: datetime


class MenuResponse(BaseModel):
    """
    메뉴 응답 모델.

    Attributes:
        id (int): 메뉴 ID.
        foods (List[FoodResponse]): 포함된 음식 목록.
        date (datetime): 메뉴 제공 날짜.
    """
    id: int
    foods: List[FoodResponse]
    date: datetime

    model_config = ConfigDict(from_attributes=True)


class MenuCounterResponse(BaseModel):
    """
    메뉴의 통계 요약 응답 모델.

    Attributes:
        menu_id (int): 조회된 메뉴의 ID.
        vote_count (int): 해당 메뉴에 포함된 음식들의 총 평가(점수) 수.
        comment_count (int): 해당 메뉴에 달린 전체 댓글 수.
    """
    menu_id: int
    vote_count: int
    comment_count: int

    model_config = ConfigDict(from_attributes=True)


class MenuStatisticResponse(BaseModel):
    """
    메뉴 통계 응답 모델.

    Attributes:
        foods_statistics (List[FoodStatisticResponse]): 각 음식에 대한 통계 정보.
        total_count (int): 모든 음식의 총 평가 수.
    """
    foods_statistics: List[FoodStatisticResponse]
    total_count: int

    model_config = ConfigDict(from_attributes=True)
