import os
import functools
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings"""
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "DeepSeek Chat API"
    
    # CORS settings
    CORS_ORIGINS: list = ["*"]
    
    # DeepSeek API settings
    DEEPSEEK_API_KEY: str = os.environ.get("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_BASE_URL: str = os.environ.get("DEEPSEEK_API_BASE_URL", "https://api.deepseek.com")
    DEEPSEEK_MODEL: str = os.environ.get("DEEPSEEK_MODEL", "deepseek-v3")

    class Config:
        env_file = ".env"
        case_sensitive = True


@functools.lru_cache()
def get_settings() -> Settings:
    """Get application settings with caching"""
    return Settings()