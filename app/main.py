import uvicorn
from fastapi import FastAPI
from config import settings
from routers.routers import router

app = FastAPI()
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run("main:app", port=settings.uvicorn_port, host=settings.uvicorn_host, reload=settings.uvicorn_restart)
