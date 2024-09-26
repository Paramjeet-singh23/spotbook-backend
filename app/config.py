from pydantic_settings import BaseSettings
from app.constant import Configuration


class Settings(BaseSettings):
    DEBUG: bool
    SECRET_KEY: str

    # FastAPI
    HOST: str
    PORT: int
    VERSION: str
    ALLOWED_HOSTS: list
    FASTAPI_DEBUG: bool

    # DATABASE
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int

    class Config:
        case_sensitive = True
        env_file = Configuration.CONFIGURATION_FILE


settings = Settings()
