from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    애플리케이션 설정 클래스.

    - 환경 변수 또는 `.env` 파일에서 값을 로드하여 설정을 관리합니다.
    """
    MYSQL_USERNAME: str
    MYSQL_PASSWORD: str
    MYSQL_HOSTNAME: str
    MYSQL_PORT: int
    MYSQL_SCHEMA: str
    
    CORS_ORIGINS: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    model_config = SettingsConfigDict(env_file=".env")
    
    
    @property
    def MYSQL_URL(self) -> str:
        return f"mysql+pymysql://{self.MYSQL_USERNAME}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOSTNAME}:{self.MYSQL_PORT}/{self.MYSQL_SCHEMA}"
    
    @property
    def cors_origin_list(self) -> str:
        return self.CORS_ORIGINS.split(",")


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
