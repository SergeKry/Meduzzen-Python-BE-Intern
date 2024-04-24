from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.schemas import users as user_schema
from app.db.database import get_session
from app.services.auth import AuthService
from app.services.users import UserService

auth_router = APIRouter(tags=['Auth'])


@auth_router.post('/auth', response_model=user_schema.Token)
async def authenticate_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                            session: AsyncSession = Depends(get_session)):
    access_token = await AuthService(session).user_authenticate(form_data.username, form_data.password)
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    return {'access_token': access_token, 'token_type': 'bearer'}


@auth_router.get('/me', response_model=user_schema.UserDetailResponse)
async def get_me(user_data: dict = Depends(AuthService().get_current_user),
                 session: AsyncSession = Depends(get_session)):
    user_id = user_data['user_id']
    user = await UserService(session).user_details(user_id)
    return user
