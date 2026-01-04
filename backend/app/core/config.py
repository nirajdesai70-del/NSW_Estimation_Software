"""
Application Configuration
"""
import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # API
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = int(os.getenv("NSW_BACKEND_PORT", "8003"))

    # Database
    DATABASE_URL: str
    DATABASE_ECHO: bool = False

    # Redis (optional)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6380/0")

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS (strict allowlist for dev)
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Legacy Reference (read-only, for comparison only)
    LEGACY_MYSQL_HOST: str = "localhost"
    LEGACY_MYSQL_PORT: int = 3306
    LEGACY_MYSQL_DB: str = "nish"
    LEGACY_MYSQL_USER: str = "root"
    LEGACY_MYSQL_PASSWORD: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


