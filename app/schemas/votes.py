from datetime import datetime
from pydantic import BaseModel, ConfigDict


class VoteCreateRequest(BaseModel):
    """
    투표 생성 요청 모델.

    Attributes:
        created_at (datetime): 투표한 날짜
        menu_id (int): 투표 대상 메뉴 ID
    """
    created_at: datetime
    menu_id: int


class VotePatchRequest(BaseModel):
    """
    투표 수정 요청 모델.

    Attributes:
        id (int): 수정할 투표 ID
        created_at (datetime): 변경할 날짜
        menu_id (int): 변경할 메뉴 ID
    """
    id: int
    created_at: datetime
    menu_id: int


class VoteCountResponse(BaseModel):
    """
    두 메뉴에 대한 투표 수를 반환하는 응답 모델.

    Attributes:
        menu1_id (int): 첫 번째 메뉴 ID.
        menu1_count (int): 첫 번째 메뉴의 투표 수.
        menu2_id (int): 두 번째 메뉴 ID.
        menu2_count (int): 두 번째 메뉴의 투표 수.
    """
    menu1_id: int
    menu1_count: int
    menu2_id: int
    menu2_count: int
    
    model_config = ConfigDict(from_attributes=True)


class VoteReponse(BaseModel):
    """
    투표 응답 모델.

    Attributes:
        id (int): 투표 ID
        user_id (str): 사용자 ID
        created_at (datetime): 투표 날짜
        menu_id (int): 메뉴 ID
    """
    id: int
    user_id: str
    created_at: datetime
    menu_id: int
    
    model_config = ConfigDict(from_attributes=True)
    