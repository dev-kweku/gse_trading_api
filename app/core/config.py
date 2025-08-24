import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_STR:str="/api/v1"
    PROJECT_NAME:str="GSE Trading Data Api"

    DATABASE_URL:str="sqlite:///./gse_trading.db"

    DATA_FILE_PATH:str="data/gse_data.csv"

    SECRET_KEY:str=os.environ.get("SECRET_KEY","your_default_secret_key")
    ACCESS_TOKEN_EXPIRE_MINUTES:int=60*24*8

    class Config:
        env_file=".env"


settings=Settings()