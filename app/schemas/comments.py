from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CommentCreateRequest(BaseModel):
    """
    댓글 작성 요청 모델.

    Attributes:
        comment (str): 작성할 댓글 내용.
        created_at (datetime): 댓글 작성 시간.
        menu_id (int): 댓글이 달릴 대상 메뉴 ID.
    """
    comment: str
    created_at: datetime
    menu_id: int


class CommentCountResponse(BaseModel):
    """
    두 메뉴에 대한 댓글 수를 반환하는 응답 모델.

    Attributes:
        menu1_id (int): 첫 번째 메뉴 ID.
        menu1_count (int): 첫 번째 메뉴의 댓글 수.
        menu2_id (int): 두 번째 메뉴 ID.
        menu2_count (int): 두 번째 메뉴의 댓글 수.
    """
    menu1_id: int
    menu1_count: int
    menu2_id: int
    menu2_count: int


class CommentResponse(BaseModel):
    """
    댓글 응답 모델.

    Attributes:
        user_id (str): 댓글 작성자의 사용자 ID.
        comment (str): 댓글 내용.
        created_at (datetime): 댓글 작성 시간.
        menu_id (int): 댓글이 달린 메뉴 ID.
    """
    user_id: str
    comment: str
    created_at: datetime
    menu_id: int

    model_config = ConfigDict(from_attributes=True)
