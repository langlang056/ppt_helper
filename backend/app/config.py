"""Application configuration management."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Keys
    llama_cloud_api_key: str
    anthropic_api_key: str

    # Paths
    upload_dir: str = "uploads"
    temp_dir: str = "temp"
    database_url: str = "sqlite+aiosqlite:///./unitutor.db"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True

    # Processing
    max_file_size_mb: int = 50
    supported_formats: list[str] = [".pdf"]

    # LLM Settings
    claude_model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 4096
    temperature: float = 0.3

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
