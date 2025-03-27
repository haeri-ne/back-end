from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from app.database import Base


class FrontLog(Base):
    """
    FrontLog (프론트엔드 로그) 테이블 모델.

    사용자의 프론트엔드 상의 행동 이벤트를 기록합니다.

    - `id`: 로그 고유 ID (PK)
    - `user_id`: 사용자 ID
    - `event_name`: 발생한 이벤트 이름 (예: click, scroll 등)
    - `event_value`: 이벤트에 대한 상세 데이터 (JSON 형식)
    - `page_name`: 이벤트가 발생한 페이지 이름
    - `event_time`: 이벤트 발생 시간
    """
    __tablename__ = "front_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    event_name = Column(String, nullable=False)
    event_value = Column(JSON, nullable=False)
    page_name = Column(String, nullable=False)
    event_time = Column(DateTime, nullable=False)

    def __repr__(self):
        """객체 정보를 문자열로 반환 (디버깅용)."""
        return f"<FrontLog(id={self.id}, user_id='{self.user_id}', event_name='{self.event_name}')>"


class BackLog(Base):
    """
    BackLog (백엔드 로그) 테이블 모델.

    백엔드에서 발생한 API 요청 및 응답 정보를 기록합니다.

    - `id`: 로그 고유 ID (PK)
    - `user_id`: 요청한 사용자 ID
    - `request_api`: 요청된 API 엔드포인트 경로
    - `status_code`: HTTP 응답 상태 코드
    - `response`: 응답 본문 (JSON 형식)
    - `is_success`: 요청 성공 여부 (`True`/`False`)
    - `time`: 로그 기록 시간
    """
    __tablename__ = "back_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    request_api = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    response = Column(JSON, nullable=False)
    is_success = Column(Boolean, nullable=False)
    time = Column(DateTime, default=datetime.now)

    def __repr__(self):
        """객체 정보를 문자열로 반환 (디버깅용)."""
        return f"<BackLog(id={self.id}, user_id='{self.user_id}', request_api='{self.request_api}')>"
