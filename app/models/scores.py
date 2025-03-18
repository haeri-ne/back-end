from datetime import datetime

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class Score(Base):
    """
    음식 점수(Score) 모델.

    특정 음식(`food_id`)에 대한 점수를 저장하며, 생성된 시간(`created_at`)이 자동으로 기록됨.
    """
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)  # ✅ UTC 기준 시간 적용

    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)

    food = relationship("Food", back_populates="scores", lazy="selectin")  

    def __repr__(self):
        """객체 정보를 문자열로 반환 (디버깅용)."""
        return f"<Score(id={self.id}, score={self.score}, food_id={self.food_id}, created_at={self.created_at})>"
