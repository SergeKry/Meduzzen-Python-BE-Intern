from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    uvicorn_host: str = Field(..., env='UVICONN_HOST')
    uvicorn_port: int = Field(..., env='UVICONN_PORT')
    uvicorn_restart: bool = Field(..., env='UVICONN_RESTART')
    db_name: str = Field(..., env='DB_NAME')
    db_user: str = Field(..., env='DB_USER')
    db_password: str = Field(..., env='DB_PASSWORD')
    db_host: str = Field(..., env='DB_HOST')
    db_port: int = Field(..., env='DB_PORT')


settings = Settings()
