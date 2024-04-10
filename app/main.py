import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from routers.routers import router

load_dotenv()

UVICORN_PORT = int(os.environ.get("UVICORN_PORT"))
UVICORN_HOST = os.environ.get("UVICORN_HOST")
UVICORN_RESTART = os.environ.get("UVICORN_RESTART", 'False').lower() == 'true'

app = FastAPI()
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run("main:app", port=UVICORN_PORT, host=UVICORN_HOST, reload=UVICORN_RESTART)

