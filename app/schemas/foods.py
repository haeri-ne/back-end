from pydantic import BaseModel, ConfigDict


class FoodCreateRequest(BaseModel):
    """
    음식 생성 요청 모델.

    Attributes:
        name (str): 생성할 음식의 이름.
    """
    name: str


class FoodPatchRequest(BaseModel):
    """
    음식 이름 수정 요청 모델.

    Attributes:
        updated_name (str): 새로 수정할 음식 이름.
    """
    updated_name: str


class FoodResponse(BaseModel):
    """
    음식 응답 모델.

    Attributes:
        id (int): 음식 ID.
        name (str): 음식 이름.
    """
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class FoodStatisticResponse(BaseModel):
    """
    음식 통계 응답 모델.

    Attributes:
        food_id (int): 음식 ID.
        count (int): 총 평가 개수.
        mean (float): 평균 점수.
        median (float): 중앙값.
        quantile_25 (float): 제1사분위수 (25%).
        quantile_75 (float): 제3사분위수 (75%).
        min (float): 최소 점수.
        max (float): 최대 점수.
    """
    food_id: int
    count: int
    mean: float
    median: float
    quantile_25: float
    quantile_75: float
    min: float
    max: float
