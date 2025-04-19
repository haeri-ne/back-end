from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from app.models.menus import Menu
from app.models.comments import Comment
from app.schemas.comments import CommentCreateRequest, CommentResponse


def create_comment(db: Session, user_id: str, comment: CommentCreateRequest) -> CommentResponse:
    """
    특정 메뉴에 대해 댓글을 생성하는 함수.

    Args:
        db (Session): SQLAlchemy 세션 객체.
        user_id (str): 댓글을 작성한 사용자 ID.
        comment (CommentCreateRequest): 댓글 내용, 생성일, 메뉴 ID 등을 포함한 요청 객체.

    Returns:
        CommentResponse: 생성된 댓글 정보.

    Raises:
        HTTPException: 주어진 menu_id가 존재하지 않을 경우 400 예외 발생.
    """
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


def get_recent_comment_by_menu(db: Session, user_id: str, menu_id: int) -> CommentResponse:
    """
    특정 메뉴에 대해 사용자가 가장 최근에 작성한 댓글을 조회합니다.

    Args:
        db (Session): SQLAlchemy 세션 객체.
        user_id (str): 사용자 ID.
        menu_id (int): 댓글이 달린 메뉴 ID.

    Returns:
        CommentResponse: 최근 댓글 정보.

    Raises:
        HTTPException: 
            - 댓글이 존재하지 않을 경우 400 에러.
    """
    comment = (
        db.query(Comment)
        .filter(and_(Comment.user_id == user_id, Comment.menu_id == menu_id))
        .order_by(Comment.id.desc())
        .first()
    )
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No comment found for this menu and user."
        )

    return CommentResponse.model_validate(comment)
