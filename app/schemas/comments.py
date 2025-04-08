from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CommentRequest(BaseModel):
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
