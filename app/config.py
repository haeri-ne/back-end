from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    애플리케이션 설정 클래스.

    - 환경 변수 또는 `.env` 파일에서 값을 로드하여 설정을 관리합니다.
    """
    SQLITE_URL: str
    CORS_ORIGINS: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    """
    설정 객체를 생성 및 캐싱.

    - `lru_cache`를 사용하여 설정을 메모리에 캐싱하여 성능을 최적화합니다.
    - 한 번 로드된 설정은 애플리케이션 실행 중 변경되지 않습니다.

    Returns:
        Settings: 애플리케이션 설정 객체.
    """
    return Settings()
