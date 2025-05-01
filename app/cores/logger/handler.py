import logging
from sqlalchemy.orm import Session
from app.models.logs import BackLog


class CustomLoggingHandler(logging.Handler):
    """
    SQLAlchemy 기반의 사용자 정의 로깅 핸들러.

    이 핸들러는 Python의 표준 logging 시스템과 연동되어 
    로그 기록을 데이터베이스에 저장합니다.

    Attributes:
        db (Session): SQLAlchemy 데이터베이스 세션.
    """

    def __init__(self, db: Session, level: int = 0) -> None:
        """
        CustomLoggingHandler 초기화.

        Args:
            db (Session): SQLAlchemy 세션 인스턴스.
            level (int): 로깅 레벨 (기본값: 0).
        """
        super().__init__(level)
        self.db = db

    def emit(self, record: logging.LogRecord) -> None:
        """
        로그 레코드를 데이터베이스에 저장.

        Args:
            record (logging.LogRecord): 로깅 시스템으로부터 전달된 로그 레코드.
        """
        try:
            new_log = BackLog(
                user_id=record.user_id,
                request_api=record.request_api,
                request_header=record.request_header,
                request_body=record.request_body,
                response=record.response,
                status_code=record.status_code,
                is_success=record.is_success,
                time=record.time
            )
            self.db.add(new_log)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        finally:
            self.db.close()
