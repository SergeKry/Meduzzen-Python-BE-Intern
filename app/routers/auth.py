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
    return user_schema.Token(**{'access_token': access_token, 'token_type': 'bearer'})


@auth_router.get('/me', response_model=user_schema.UserDetailResponse)
async def get_me(user_data: dict = Depends(AuthService().get_current_user),
                 session: AsyncSession = Depends(get_session)):
    user = await UserService(session).user_details_by_email(user_data['email'])
    if not user:
        user = await UserService(session).create_user_from_auth0(user_data)
    return user
