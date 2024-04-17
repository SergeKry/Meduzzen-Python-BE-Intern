from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.db.database import get_session
from app.schemas import users as user_schema
from app.repository import users as db

users_router = APIRouter(prefix='/users', tags=['Users'])


@users_router.post('/', status_code=status.HTTP_201_CREATED)
async def add_user(user: user_schema.SignUpRequest, session: AsyncSession = Depends(get_session)):
    await db.create_user(user, session)


@users_router.get('/')  # response_model=List[user_schema.UserListResponse]
async def read_all_users(session: AsyncSession = Depends(get_session)):
    all_users = await db.get_all_users(session)
    return all_users


@users_router.get('/{user_id}')
async def read_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await db.get_user_by_id(user_id, session)
    return user


@users_router.put('/{user_id}', status_code=status.HTTP_200_OK)
async def update_user(user_id: int,
                      request_body: user_schema.UserUpdateRequest,
                      session: AsyncSession = Depends(get_session)):
    await db.user_update(user_id, request_body, session)


@users_router.delete('/{user_id}', status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    await db.user_delete(user_id, session)
