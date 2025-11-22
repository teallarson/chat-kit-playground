import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    anthropic_api_key: str = ""
    openai_api_key: str = ""
    host: str = "0.0.0.0"
    port: int = 8000
    frontend_url: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        # Look for .env file in the backend directory (where this config file lives)
        # Path(__file__) = backend/app/config.py
        # .parent.parent = backend/
        env_file=Path(__file__).parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    settings = Settings()
    
    # Set OPENAI_API_KEY in environment for libraries that check os.environ directly
    # This is needed because openai.agents checks os.environ.get("OPENAI_API_KEY")
    if settings.openai_api_key and not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = settings.openai_api_key
    
    return settings


# Load settings immediately when module is imported to set environment variables early
_settings = get_settings()
