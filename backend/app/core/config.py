SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGE_ME")import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ConstructPulse API"
    VERSION: str = "1.1.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGE_ME")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    DATABASE_URL: str = os.getenv("DATABASE_URL", "CHANGE_ME")

    class Config:
        env_file = ".env"

settings = Settings()
