from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./insightx.db"
    SECRET_KEY: str = "super-secret-insight-x-jwt-key-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    STRUCTURING_THRESHOLD: float = 500000.0
    STRUCTURING_WINDOW_MINUTES: int = 60
    STRUCTURING_MIN_TRANSACTIONS: int = 3
    INSIDER_WINDOW_MINUTES: int = 30
    NEW_BENEFICIARY_WINDOW_MINUTES: int = 60
    WORK_START_HOUR: int = 9
    WORK_END_HOUR: int = 18

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()