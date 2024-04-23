from datetime import timedelta, datetime
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import utils
from app.repository.users import UserRepository


oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/users/auth', scheme_name='JWT')


class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(self.session)

    async def user_details(self, user_id: int):
        user = await self.user_repository.get_one_by_id(user_id)
        return user

    async def get_all_users(self):
        users = await self.user_repository.get_all()
        return {'users': users}

    async def add_user(self, user):
        user_dict = user.dict()
        if await self.user_repository.get_one_by_username(user_dict['username']):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Username already exists')
        if await self.user_repository.get_one_by_email(user_dict['email']):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already exists')
        hashed_password = utils.encrypt_password(user_dict.pop("password2"))
        user_dict.update({'password': hashed_password})
        new_user = await self.user_repository.create_one(user_dict)
        return new_user

    async def update_user(self, user_id, new_values):
        new_values_dict = new_values.dict(exclude_unset=True)
        if await self.user_repository.get_one_by_username(new_values_dict.get('username')):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Username already exists')
        if await self.user_repository.get_one_by_email(new_values_dict.get('email')):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already exists')
        if new_values_dict.get('password'):
            hashed_password = utils.encrypt_password(new_values_dict.pop("password2"))
            new_values_dict.update({'password': hashed_password})
        await self.user_repository.update_one(user_id, new_values_dict)

    async def delete_user(self, user_id) -> None:
        user = await self.user_repository.get_one_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        await self.user_repository.delete_one(user_id)

    async def user_authenticate(self, username, password):
        user = await self.user_repository.get_one_by_username(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        if not utils.validate_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect password')
        token = utils.create_access_token(user.username, user.email, user.id, timedelta(minutes=30))
        return token


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = utils.decode_access_token(token)
        username: str = payload.get('sub')
        email: str = payload.get('email')
        user_id: int = payload.get('user_id')
        if username is None or email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
        if datetime.fromtimestamp(payload.get('exp')) < datetime.now():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Token expired')
        return {'username': username, 'email': email, 'user_id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')


