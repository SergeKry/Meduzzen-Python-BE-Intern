from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_session
from app.schemas import users as user_schema
from app.services.auth import AuthService


health_router = APIRouter()

db_dependency = Annotated[AsyncSession, Depends(get_session)]
user_dependency = Annotated[user_schema.User, Depends(AuthService().get_current_user)]

token_auth_scheme = HTTPBearer()
token_dependency = Annotated[HTTPAuthorizationCredentials, Depends(token_auth_scheme)]

@health_router.get("/")
async def healthcheck():
    return {"status_code": "200", "detail": "ok", "result": "working"}