from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Score(Base):
    """
    Score (음식 점수) 테이블 모델.

    Attributes:
        id (int): 점수 고유 ID (Primary Key).
        user_id (str): 점수를 매긴 사용자 ID.
        score (float): 평가 점수 (예: 1.0 ~ 5.0).
        created_at (datetime): 점수 생성 시각.
        food_id (int): 점수를 매긴 대상 음식의 ID (Foreign Key).
        food (Food): 해당 점수가 연결된 음식 객체.
    """
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())

    food_id = Column(Integer, ForeignKey("foods.id"))
    food = relationship("Food", back_populates="scores", lazy="selectin")

    def __repr__(self):
        """
        점수 객체 정보를 문자열로 반환합니다.

        Returns:
            str: 점수 ID, 값, 생성일, 음식 ID를 포함한 문자열 표현.
        """
        return f"<Score(id={self.id}, score={self.score}, created_at={self.created_at}, food_id={self.food_id})>"
