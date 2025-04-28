from pydantic import BaseSettings, PostgresDsn, RedisDsn, Field

class Settings(BaseSettings):
    database_url: PostgresDsn = Field(..., env='DATABASE_URL')
    redis_url: RedisDsn = Field(..., env='REDIS_URL')
    secret_key: str = Field(..., env='SECRET_KEY')

    class Config:
        env_file = '.env'
        case_sensitive = False

settings = Settings()