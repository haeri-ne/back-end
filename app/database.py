from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import get_settings

settings = get_settings()

engine = create_engine(settings.MYSQL_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()


def init_db():
    """
    데이터베이스 및 테이블 초기화 함수.
    `Base.metadata.create_all(bind=engine)`을 호출하여 테이블을 생성함.
    """
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    SQLAlchemy 세션을 제공하는 FastAPI 의존성 함수.

    Yields:
        Session: SQLAlchemy 데이터베이스 세션.

    Raises:
        Exception: 세션 중 오류 발생 시 롤백 후 예외 발생.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()