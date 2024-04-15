import uvicorn
from fastapi import FastAPI
from config import settings
from routers.routers import router

app = FastAPI()
app.include_router(router, tags=['Healthcheck'])


if __name__ == '__main__':
    uvicorn.run("main:app", port=settings.UVICORN_PORT, host=settings.UVICORN_HOST, reload=settings.UVICORN_RESTART)
