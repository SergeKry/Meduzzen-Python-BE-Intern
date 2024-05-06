import uvicorn
from fastapi import FastAPI
from config import settings
from routers import routers, users, auth, companies, actions, quiz


app = FastAPI()
app.include_router(routers.health_router, tags=['Healthcheck'])
app.include_router(auth.auth_router)
app.include_router(users.users_router)
app.include_router(companies.company_router)
app.include_router(actions.action_router)
app.include_router(quiz.quiz_router)

if __name__ == '__main__':
    uvicorn.run("main:app", port=settings.UVICORN_PORT, host=settings.UVICORN_HOST, reload=settings.UVICORN_RESTART)
