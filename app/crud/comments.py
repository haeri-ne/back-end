from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.menus import Menu
from app.models.comments import Comment
from app.schemas.comments import CommentRequest, CommentResponse


def create_comment(db: Session, user_id: str, comment: CommentRequest) -> CommentResponse:
    """
    특정 메뉴에 대해 댓글을 생성하는 함수.

    Args:
        db (Session): SQLAlchemy 세션 객체.
        user_id (str): 댓글을 작성한 사용자 ID.
        comment (CommentRequest): 댓글 내용, 생성일, 메뉴 ID 등을 포함한 요청 객체.

    Returns:
        CommentResponse: 생성된 댓글 정보.

    Raises:
        HTTPException: 주어진 menu_id가 존재하지 않을 경우 400 예외 발생.
    """
    # 댓글이 달릴 메뉴가 존재하는지 검증
    if not db.query(Menu).filter(Menu.id == comment.menu_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid menu_id. Menu does not exist."
        )
    
    new_comment = Comment(
        user_id=user_id,
        comment=comment.comment,
        created_at=comment.created_at,
        menu_id=comment.menu_id
    )

    db.add(new_comment)
    db.flush()

    return CommentResponse.model_validate(new_comment)
