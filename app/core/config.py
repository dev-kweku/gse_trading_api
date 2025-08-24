import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "GSE Trading Data API"
    
    # Database
    DATABASE_URL: str = "sqlite:///./gse_trading.db"
    
    # File paths - use relative path to the data directory
    DATA_FILE_PATH: str = "data-log/gse_data.csv"
    
    # Security
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    class Config:
        env_file = ".env"

settings = Settings()