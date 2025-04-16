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
