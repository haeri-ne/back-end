from sqlalchemy.orm import Session

from fastapi import APIRouter, HTTPException, Depends, status

from app.database import get_db
from app.dependencies.user import get_user_id
from app.crud import comments
from app.schemas.comments import CommentCreateRequest, CommentCountResponse, CommentResponse


router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment: CommentCreateRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_user_id)
):
    """s
    메뉴에 대한 댓글을 작성하는 API.

    Args:
        comment (CommentCreateRequest): 작성할 댓글 정보.
        db (Session): SQLAlchemy 세션 객체.
        user_id (str): 요청자 사용자 ID (헤더에서 추출).

    Returns:
        CommentResponse: 생성된 댓글 정보.

    Raises:
        HTTPException: 댓글 저장에 실패할 경우 500 예외 발생.
    """
    new_comment = comments.create_comment(db, user_id, comment)

    if not new_comment:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create comment"
        )

    return new_comment


@router.get("/{menu_id}", response_model=CommentResponse, status_code=status.HTTP_200_OK)
async def get_comment_by_menu(
    menu_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_user_id)
):
    """
    특정 메뉴에 대해 사용자가 가장 최근에 작성한 댓글을 조회하는 API.

    Args:
        menu_id (int): 조회 대상 메뉴 ID.
        db (Session): SQLAlchemy 세션 객체.
        user_id (str): 요청 사용자 ID (헤더에서 추출).

    Returns:
        CommentResponse: 최근 댓글 정보.

    Raises:
        HTTPException: 해당 메뉴에 대한 댓글이 존재하지 않을 경우.
    """
    comment = comments.get_comment_by_menu(db, user_id, menu_id)
    return comment


@router.get("/count", response_model=CommentCountResponse, status_code=status.HTTP_200_OK)
async def get_comment_count(
    menu1_id: int,
    menu2_id: int,
    db: Session = Depends(get_db)
):
    """
    두 개의 메뉴에 대한 댓글 수를 조회하는 API.

    쿼리 파라미터로 전달된 menu1_id, menu2_id에 대한 댓글 수를 각각 계산하여 반환합니다.

    Args:
        menu1_id (int): 첫 번째 메뉴 ID.
        menu2_id (int): 두 번째 메뉴 ID.
        db (Session): SQLAlchemy 세션 객체.

    Returns:
        CommentCountResponse: 두 메뉴의 ID와 각각의 투표 수.

    Raises:
        HTTPException: 하나라도 존재하지 않는 메뉴 ID가 있을 경우 400 예외 발생.
    """
    comment_count = comments.get_comment_count(db, menu1_id, menu2_id)
    return comment_count
