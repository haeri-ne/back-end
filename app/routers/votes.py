from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.user import get_user_id
from app.crud import votes
from app.schemas.votes import (
    VoteCreateRequest, 
    VotePatchRequest, 
    VoteCountResponse,
    VoteReponse
)


router = APIRouter(
    prefix="/votes", 
    tags=["votes"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=VoteReponse, status_code=status.HTTP_201_CREATED)
async def create_vote(
    vote: VoteCreateRequest, 
    db: Session = Depends(get_db),
    user_id: str = Depends(get_user_id)
):
    """
    새로운 투표를 생성합니다.

    - 클라이언트는 메뉴 ID와 투표 날짜(created_at)를 전달합니다.
    - user_id는 요청 헤더에서 받아 사용자의 투표로 저장됩니다.

    Args:
        vote (VoteCreateRequest): 생성할 투표 정보.
        db (Session): 데이터베이스 세션.
        user_id (str): 요청자의 식별자 (헤더에서 추출).

    Returns:
        VoteReponse: 생성된 투표 객체.
    """
    new_vote = votes.create_vote(db, user_id, vote)
    return new_vote


@router.get("/count", response_model=VoteCountResponse, status_code=status.HTTP_200_OK)
async def get_vote_count(
    menu1_id: int,
    menu2_id: int,
    db: Session = Depends(get_db)
):
    """
    두 개의 메뉴에 대한 투표 수를 조회하는 API.

    쿼리 파라미터로 전달된 menu1_id, menu2_id에 대한 투표 수를 각각 계산하여 반환합니다.

    Args:
        menu1_id (int): 첫 번째 메뉴 ID.
        menu2_id (int): 두 번째 메뉴 ID.
        db (Session): SQLAlchemy 세션 객체.

    Returns:
        VoteCountResponse: 두 메뉴의 ID와 각각의 투표 수.

    Raises:
        HTTPException: 하나라도 존재하지 않는 메뉴 ID가 있을 경우 400 예외 발생.
    """
    vote_count = votes.get_vote_count(db, menu1_id, menu2_id)
    return vote_count


@router.get("/{menu_id}", response_model=VoteReponse, status_code=status.HTTP_200_OK)
async def get_vote(
    menu_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_user_id)
):
    """
    특정 메뉴에 대한 사용자의 투표를 조회합니다.

    - menu_id와 user_id를 조합하여 고유 투표를 조회합니다.

    Args:
        menu_id (int): 조회할 메뉴 ID.
        db (Session): 데이터베이스 세션.
        user_id (str): 요청자의 식별자.

    Returns:
        VoteReponse: 해당 메뉴에 대한 사용자의 투표 정보.
    """
    vote = votes.get_vote(db, user_id, menu_id)
    return vote


@router.patch("/", response_model=VoteReponse, status_code=status.HTTP_200_OK)
async def update_vote(
    vote: VotePatchRequest, 
    db: Session = Depends(get_db),
    user_id: str = Depends(get_user_id)
):
    """
    사용자가 본인의 투표를 수정합니다.

    - vote_id를 기준으로 해당 투표를 찾아 수정하며, user_id 일치 여부를 검증합니다.

    Args:
        vote (VotePatchRequest): 수정할 투표 정보 (id, created_at, menu_id 포함).
        db (Session): 데이터베이스 세션.
        user_id (str): 요청자의 식별자 (헤더에서 추출).

    Returns:
        VoteReponse: 수정된 투표 정보.

    Raises:
        HTTPException: 
            - 존재하지 않는 vote_id일 경우 (400)
            - 본인의 투표가 아닐 경우 (403)
    """
    updated_vote = votes.update_vote(db, user_id, vote)
    return updated_vote
