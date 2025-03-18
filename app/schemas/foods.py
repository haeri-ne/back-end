from pydantic import BaseModel, ConfigDict

class FoodCreateRequest(BaseModel):
    """음식 생성 요청"""
    name: str
    
class FoodResponse(BaseModel):
    """음식 응답 모델"""
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
