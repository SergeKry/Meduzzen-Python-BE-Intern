from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

# class Settings(BaseSettings):
#     uvicorn_host: str = Field(..., env='UVICORN_HOST')
#     uvicorn_port: int = Field(..., env='UVICORN_PORT')
#     uvicorn_restart: bool = Field(..., env='UVICORN_RESTART')
#     db_name: str = Field(..., env='DB_NAME')
#     db_user: str = Field(..., env='DB_USER')
#     db_password: str = Field(..., env='DB_PASSWORD')
#     db_host: str = Field(..., env='DB_HOST')
#     db_port: int = Field(..., env='DB_PORT')
#     redis_host: str = Field(..., env='REDIS_HOST')
#     redis_port: int = Field(..., env='REDIS_PORT')


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


settings = Settings()
