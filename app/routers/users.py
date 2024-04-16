from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.schemas.user import SignUpRequest

users_router = APIRouter(prefix='/users', tags=['Users'])


@users_router.post('/')
async def create_user(user: SignUpRequest, session: AsyncSession = Depends(get_session)):
    pass  # database create function should be here. We should pass user and session to DB function


@users_router.get('/')
async def read_users(session: AsyncSession = Depends(get_session)):
    pass  # need to add validation model
