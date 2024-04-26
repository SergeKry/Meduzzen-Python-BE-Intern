from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    UVICORN_HOST: str
    UVICORN_PORT: int
    UVICORN_RESTART: bool

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: int

    JWT_ALGORITHM: str
    JWT_ACCESS_SECRET: str
    JWT_ACCESS_EXPIRATION: int
    JWT_AUD: str


settings = Settings()
