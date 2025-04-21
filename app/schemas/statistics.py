from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class FoodMeanStatisticResponse(BaseModel):
    """
    음식 평균 통계 응답 모델.

    Attributes:
        food_id (int): 음식 ID.
        mean (float): 해당 음식의 평균 점수.
    """
    food_id: int
    mean: float


class StatisticsDetail(BaseModel):
    """
    통계 세부 정보 모델.

    Attributes:
        scores (dict): 점수 분포 딕셔너리.
        total (int): 총 평가 개수.
        mean (float): 평균 점수.
        median (float): 중앙값.
        quantile_25 (float): 제1사분위수 (25%).
        quantile_75 (float): 제3사분위수 (75%).
        min (float): 최소 점수.
        max (float): 최대 점수.
    """
    scores: dict
    total: int
    mean: float
    median: float
    quantile_25: float
    quantile_75: float
    min: float
    max: float


class FoodStatisticsIncludingDuplicate(StatisticsDetail):
    """
    중복 포함 음식 통계 모델.
    
    StatisticsDetail을 상속받아 동일한 속성을 사용합니다.
    """
    pass


class FoodStatisticsWithoutDuplicate(StatisticsDetail):
    """
    중복 제거 음식 통계 모델.
    
    StatisticsDetail을 상속받아 동일한 속성을 사용합니다.
    """
    pass


class FoodStatisticResponse(BaseModel):
    """
    음식 통계 응답 모델.

    Attributes:
        food_id (int): 음식 ID.
        statistics_including_duplicates (FoodStatisticsIncludingDuplicate): 중복 포함 통계.
        statistics_without_duplicates (FoodStatisticsWithoutDuplicate): 중복 제거 통계.
    """
    food_id: int
    statistics_including_duplicates: FoodStatisticsIncludingDuplicate
    statistics_without_duplicates: FoodStatisticsWithoutDuplicate


class MenuMeanStatisticResponse(BaseModel):
    """
    메뉴별 음식 평균 통계 응답 모델.

    Attributes:
        menu_id (int): 메뉴 ID.
        foods_statistics (List[FoodMeanStatisticResponse]): 각 음식의 평균 통계 목록.
        date (datetime): 통계가 생성된 날짜.
    """
    menu_id: int
    foods_statistics: List[FoodMeanStatisticResponse]
    date: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class MenuStatisticResponse(BaseModel):
    """
    메뉴 통계 응답 모델.

    Attributes:
        foods_statistics (List[FoodStatisticResponse]): 각 음식에 대한 통계 정보 목록.
        total_count_including_duplicates (int): 중복 포함 전체 평가 수.
        total_count_without_duplicates (int): 중복 제거 전체 평가 수.
        total_avg_including_duplicates (float): 중복 포함 전체 평균 점수.
        total_avg_without_duplicates (float): 중복 제거 전체 평균 점수.
    """
    foods_statistics: List[FoodStatisticResponse]
    total_count_including_duplicates: int
    total_count_without_duplicates: int
    total_avg_including_duplicates: float
    total_avg_without_duplicates: float

    model_config = ConfigDict(from_attributes=True)
