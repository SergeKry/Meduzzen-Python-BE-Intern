from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.db.database import get_session
from app.schemas import users as user_schema
from app.repository import users as db
from app.services import users as services

users_router = APIRouter(prefix='/users', tags=['Users'])


@users_router.post('/', status_code=status.HTTP_201_CREATED)
async def add_user(user: user_schema.SignUpRequest, session: AsyncSession = Depends(get_session)):
    await services.add_user(user, session)


@users_router.get('/')
async def read_all_users(session: AsyncSession = Depends(get_session)) -> user_schema.UserListResponse:
    all_users = await services.get_all_users(session)
    return all_users


@users_router.get('/{user_id}')
async def read_user(user_id: int, session: AsyncSession = Depends(get_session)) -> user_schema.UserDetailResponse:
    user = await services.user_details(user_id, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user


@users_router.put('/{user_id}', status_code=status.HTTP_200_OK)
async def update_user(user_id: int,
                      request_body: user_schema.UserUpdateRequest,
                      session: AsyncSession = Depends(get_session)):
    user = await db.get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    await services.update_user(user_id, request_body, session)


@users_router.delete('/{user_id}', status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    await services.delete_user(user_id, session)
