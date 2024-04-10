from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    uvicorn_host: str = os.environ.get('UVICONN_HOST', '0.0.0.0')
    uvicorn_port: int = os.environ.get('UVICONN_PORT', 8000)
    uvicorn_restart: bool = os.environ.get('UVICONN_RESTART', True)


settings = Settings()