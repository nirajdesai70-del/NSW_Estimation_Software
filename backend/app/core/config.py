"""
Application Configuration
"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(
        env_file="backend/.env",
        case_sensitive=True,
        extra="ignore",  # Ignore unknown env vars (e.g., Laravel's RAG_FEEDBACK_*)
    )

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # API
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = int(os.getenv("NSW_BACKEND_PORT", "8003"))

    # Database - safe defaults for dev/test (override via env in production)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    DATABASE_ECHO: bool = False

    # Redis (optional)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6380/0")

    # Security - safe default for dev/test (override via env in production)
    SECRET_KEY: str = "dev-only-secret-change-me-in-production"
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


@lru_cache
def get_settings() -> Settings:
    """Get cached Settings instance (prevents import-time failures)."""
    return Settings()


# Backwards compatibility: keep settings for code that imports it directly
# For new code, prefer using get_settings() instead
settings = get_settings()


