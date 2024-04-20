from fastapi import HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import utils
from app.repository.users import UserRepository
from app.db import models as db_model


class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def user_details(self, user_id: int) -> db_model.User:
        user = await UserRepository(self.session).get_one_by_id(user_id)
        return user

    async def get_all_users(self):
        users = await UserRepository(self.session).get_all()
        print(type(users))
        return {'users': users}

    async def add_user(self, user) -> None:
        user_dict = user.dict()
        password = user_dict['password'] == user_dict['password2']
        if not password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
        new_user = UserRepository(self.session)
        if await new_user.get_one_by_username(user_dict['username']):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Username already exists')
        if await new_user.get_one_by_email(user_dict['email']):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already exists')
        hashed_password, salt = utils.encrypt_password(user_dict.pop("password2"))
        user_dict.update({'password': hashed_password, 'salt': salt})
        await new_user.create_one(user_dict)

    async def update_user(self, user_id, new_values) -> None:
        new_values_dict = new_values.dict(exclude_unset=True)
        password = new_values_dict.get('password') == new_values_dict.get('password2')
        if not password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
        user = UserRepository(self.session)
        if await user.get_one_by_username(new_values_dict.get('username')):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Username already exists')
        if await user.get_one_by_email(new_values_dict.get('email')):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already exists')
        if new_values_dict.get('password'):
            hashed_password, salt = utils.encrypt_password(new_values_dict.pop("password2"))
            new_values_dict.update({'password': hashed_password, 'salt': salt})
        await user.update_one(user_id, new_values_dict)

    async def delete_user(self, user_id) -> None:
        user = await UserRepository(self.session).get_one_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        await UserRepository(self.session).delete_one(user_id)
