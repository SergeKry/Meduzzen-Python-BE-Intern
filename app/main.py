import uvicorn
from fastapi import FastAPI
from config import settings
from routers.routers import health_router, users_router, auth_router

app = FastAPI()
app.include_router(health_router, tags=['Healthcheck'])
app.include_router(auth_router)
app.include_router(users_router)


if __name__ == '__main__':
    uvicorn.run("main:app", port=settings.UVICORN_PORT, host=settings.UVICORN_HOST, reload=settings.UVICORN_RESTART)
