from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/reviewflow"
    
    # Model settings
    MODEL_PATH: str = "distilbert-base-uncased-finetuned-sst-2-english"
    
    # Rate limiting settings
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Review validation
    MIN_REVIEW_LENGTH: int = 10
    MAX_REVIEW_LENGTH: int = 2000
    MIN_RATING: int = 1
    MAX_RATING: int = 5
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings() 