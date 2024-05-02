from fastapi import HTTPException
from jose import JWTError
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import utils
from app.repository.users import UserRepository
from app.schemas import users as user_schema
from app.utils.utils import decode_access_token
import app.db.user as db_model


class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(self.session)

    async def get_current_user(self, token):
        """Get real user id from database here"""
        try:
            token_user_id, token_email, token_username = decode_access_token(token.credentials)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token invalid')
        current_user = await UserService(self.session).user_details_by_email(token_email)
        return current_user


    async def user_details_by_id(self, user_id: int):
        user = await self.user_repository.get_one_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        return user

    async def user_details_by_email(self, email: str):
        user = await self.user_repository.get_one_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
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

    async def create_user_from_auth0(self, user: user_schema.User) -> db_model.User:
        hashed_random_password = utils.generate_random_password()
        new_user = user_schema.SignUpRequest(username=user.username, email=user.email, password=hashed_random_password,
                                             password2=hashed_random_password)
        user_dict = new_user.dict()
        user_dict.pop('password2')
        new_user = await self.user_repository.create_one(user_dict)
        return new_user

    async def update_user(self, user_id, new_values) -> None:
        new_values_dict = new_values.dict(exclude_unset=True)
        if await self.user_repository.get_one_by_username(new_values_dict.get('username')):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Username already exists')
        if new_values_dict.get('password'):
            hashed_password = utils.encrypt_password(new_values_dict.pop("password2"))
            new_values_dict.update({'password': hashed_password})
        await self.user_repository.update_one(user_id, new_values_dict)

    async def delete_user(self, user_id) -> None:
        user = await self.user_repository.get_one_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        await self.user_repository.delete_one(user_id)
