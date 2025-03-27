import logging
from app.database import get_db
from app.cores.logger.handler import CustomLoggingHandler


def setup_logger() -> logging.Logger:
    """
    커스텀 로그 핸들러를 포함한 로거를 설정하는 함수.

    DB 세션을 통해 CustomLoggingHandler를 생성하고,
    로거에 핸들러를 추가하여 로그 메시지를 데이터베이스에 저장할 수 있도록 설정합니다.

    Returns:
        logging.Logger: 커스텀 핸들러가 등록된 로거 인스턴스.
    """
    handler = CustomLoggingHandler(db=next(get_db()))
    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


# 애플리케이션 전체에서 사용할 전역 로거 객체
logger = setup_logger()
