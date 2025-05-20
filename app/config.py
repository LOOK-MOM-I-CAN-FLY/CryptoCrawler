import os
from pydantic import BaseSettings, PostgresDsn, Field

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    REDIS_URL: str
    SECRET_KEY: str

    class Config:
        env_file = '.env'
        case_sensitive = False

settings = Settings()