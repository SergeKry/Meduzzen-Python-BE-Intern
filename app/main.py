import uvicorn
from fastapi import FastAPI
from config import settings
from routers import routers
from routers import users
from routers import auth
from routers import companies

app = FastAPI()
app.include_router(routers.health_router, tags=['Healthcheck'])
app.include_router(auth.auth_router)
app.include_router(users.users_router)
app.include_router(companies.company_router)

if __name__ == '__main__':
    uvicorn.run("main:app", port=settings.UVICORN_PORT, host=settings.UVICORN_HOST, reload=settings.UVICORN_RESTART)
