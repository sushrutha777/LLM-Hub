import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "LLMHub API"
    API_V1_STR: str = "/api/v1"
    
    # SECURITY
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week
    ALGORITHM: str = "HS256"

    # DATABASE
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./llmhub.db")
    
    # REDIS
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    class Config:
        case_sensitive = True

settings = Settings()
