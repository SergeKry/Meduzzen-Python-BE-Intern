from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.db.database import get_session
from app.schemas import users as user_schema
from app.services.users import UserService
from app.services.auth import AuthService

users_router = APIRouter(prefix='/users', tags=['Users'])

user_dependency = Annotated[user_schema.User, Depends(AuthService().get_current_user)]


@users_router.post('/', status_code=status.HTTP_201_CREATED)
async def add_user(user: user_schema.SignUpRequest,
                   session: AsyncSession = Depends(get_session)) -> user_schema.UserDetailResponse:
    new_user = await UserService(session).add_user(user)
    return new_user


@users_router.get('/')
async def read_all_users(session: AsyncSession = Depends(get_session)) -> user_schema.UserListResponse:
    all_users = await UserService(session).get_all_users()
    return all_users


@users_router.get('/{user_id}')
async def read_user(user_id: int, session: AsyncSession = Depends(get_session)) -> user_schema.UserDetailResponse:
    user = await UserService(session).user_details_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user


@users_router.patch('/{user_id}', status_code=status.HTTP_200_OK)
async def update_user(user: user_dependency, user_id: int,
                      request_body: user_schema.UserUpdateRequest,
                      session: AsyncSession = Depends(get_session)) -> user_schema.UserDetailResponse:
    if user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Don't have permission to update user")
    await UserService(session).update_user(user_id, request_body)
    return await UserService(session).user_details_by_id(user_id)


@users_router.delete('/{user_id}', status_code=status.HTTP_200_OK)
async def delete_user(user: user_dependency, user_id: int,
                      session: AsyncSession = Depends(get_session)) -> user_schema.ConfirmationResponse:
    if user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Don't have permission to delete user")
    await UserService(session).delete_user(user_id)
    return user_schema.ConfirmationResponse(message='User deleted')
