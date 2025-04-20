from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from app.models.menus import Menu
from app.models.votes import Vote
from app.schemas.votes import (
    VoteCreateRequest, 
    VotePatchRequest, 
    VoteCountResponse,
    VoteReponse
)


def create_vote(db: Session, user_id: str, vote: VoteCreateRequest) -> VoteReponse:
    """
    투표를 새로 생성합니다.

    Args:
        db (Session): DB 세션
        user_id (str): 사용자 ID (헤더에서 추출)
        vote (VoteCreateRequest): 생성 요청 정보

    Returns:
        VoteReponse: 생성된 투표 정보

    Raises:
        HTTPException:
            - 존재하지 않는 메뉴일 경우 400 에러
            - 이미 해당 메뉴에 투표한 경우 400 에러
    """
    if not db.query(Menu).filter(Menu.id == vote.menu_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid menu_id. Menu does not exist."
        )
        
    if db.query(Vote).filter(Vote.menu_id == vote.menu_id, Vote.user_id == user_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already voted for this menu."
        )
        
    new_vote = Vote(
        user_id=user_id,
        created_at=vote.created_at,
        menu_id=vote.menu_id
    )

    db.add(new_vote)
    db.flush()

    return VoteReponse.model_validate(new_vote)


def get_vote(db: Session, user_id: str, menu_id: int) -> VoteReponse:
    """
    특정 사용자의 특정 메뉴에 대한 투표 조회.

    Args:
        db (Session): DB 세션
        user_id (str): 사용자 ID
        menu_id (int): 조회할 메뉴 ID

    Returns:
        VoteReponse: 조회된 투표 정보

    Raises:
        HTTPException: 존재하지 않는 투표일 경우 400 에러
    """
    vote = db.query(Vote).filter(and_(Vote.user_id == user_id, Vote.menu_id == menu_id)).first()
    
    if not vote:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vote does not exist."
        )
    
    return VoteReponse.model_validate(vote)


def get_vote_count(db: Session, menu1_id: int, menu2_id: int) -> VoteCountResponse:
    """
    두 개의 메뉴에 대한 투표 수를 계산합니다.

    Args:
        db (Session): SQLAlchemy 세션 객체.
        menu1_id (int): 첫 번째 메뉴 ID.
        menu2_id (int): 두 번째 메뉴 ID.
        
    Returns:
        VoteCountResponse: 각 메뉴의 투표 수.

    Raises:
        HTTPException: 존재하지 않는 메뉴가 포함된 경우.
    """
    if not (
        db.query(Menu).filter(Menu.id == menu1_id).first() and
        db.query(Menu).filter(Menu.id == menu2_id).first()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Menu does not exist."
        )
        
    menu1_count = db.query(Vote).filter(Vote.menu_id == menu1_id).count()
    menu2_count = db.query(Vote).filter(Vote.menu_id == menu2_id).count()
    
    return VoteCountResponse.model_validate({
        "menu1_id": menu1_id,
        "menu1_count": menu1_count,
        "menu2_id": menu2_id,
        "menu2_count": menu2_count,
    })


def update_vote(db: Session, new_vote: VotePatchRequest) -> VoteReponse:
    """
    본인의 투표 정보를 수정합니다.

    Args:
        db (Session): DB 세션
        new_vote (VotePatchRequest): 수정할 투표 정보

    Returns:
        VoteReponse: 수정된 투표 정보

    Raises:
        HTTPException: 
            - 투표가 존재하지 않으면 400 에러
    """
    vote = db.query(Vote).filter(Vote.id == new_vote.id).first()
    
    if not vote:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid vote_id. Vote does not exist."
        )

    if vote.menu_id != new_vote.menu_id:
        vote.created_at = new_vote.created_at
        vote.menu_id = new_vote.menu_id

        db.commit()
        db.refresh(vote)

    return VoteReponse.model_validate(vote)
