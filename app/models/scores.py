from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Score(Base):
    """
    Score (음식 점수) 테이블 모델.

    Attributes:
        id (Integer): 점수 고유 ID (Primary Key)
        user_id (String(100)): 사용자 식별자 (UUID)
        score (float): 평가 점수 (0.0 ~ 5.0)
        created_at (DateTime): 점수 생성 일자
        food_id (int): 점수를 매긴 대상 음식의 ID (Foreign Key)
        food (Food): 해당 점수 매겨진 음식 객체 (1:N 관계)
    """
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), nullable=False)
    score = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)

    food_id = Column(Integer, ForeignKey("foods.id"))
    food = relationship("Food", back_populates="scores", lazy="selectin")

    def __repr__(self):
        """객체 정보를 문자열로 반환 (디버깅용)."""
        return f"<Score(id={self.id}, score={self.score}, created_at={self.created_at}, food_id={self.food_id})>"
