from datetime import datetime

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class Score(Base):
    """
    Score (음식 점수) 테이블 모델.

    - `id`: 점수 ID (PK)
    - `score`: 평가 점수
    - `created_at`: 점수 생성 날짜
    - `food_id`: 평가 대상 음식 (FK)
    """
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())

    food_id = Column(Integer, ForeignKey("foods.id"))
    food = relationship("Food", back_populates="scores", lazy="selectin")

    def __repr__(self):
        """객체 정보를 문자열로 반환 (디버깅용)."""
        return f"<Score(id={self.id}, score={self.score}, created_at={self.created_at}, food_id={self.food_id})>"
