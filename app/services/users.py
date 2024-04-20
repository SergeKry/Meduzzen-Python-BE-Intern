from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status

from app.schemas import users as user_schema
from app.utils import utils
from app.repository.users import UserRepository


async def user_details(user_id: int, session):
    user = await UserRepository(session).get_one_by_id(user_id)
    return user


async def get_all_users(session):
    users = await UserRepository(session).get_all()
    return {'users': users}


async def add_user(user, session):
    user_dict = user.dict()
    password = user_dict['password'] == user_dict['password2']
    email = utils.validate_email(user_dict['email'])
    role = user_dict['role'] in (0, 1, 2)
    if password and email and role:
        user_dict = user.dict()
        hashed_password, salt = utils.encrypt_password(user_dict.pop("password2"))
        user_dict.update({'password': hashed_password, 'salt': salt})
        try:
            user = UserRepository(session)
            await user.create_one(user_dict)
        except IntegrityError as err:
            error_detail = str(err.args).split('DETAIL:')[-1].strip()[:-4]
            raise HTTPException(status_code=500, detail=error_detail)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


async def update_user(user_id, user, session):
    user_dict = user.dict()
    password = user_dict['password'] == user_dict['password2']
    email = utils.validate_email(user_dict['email'])
    role = user_dict['role'] in (0, 1, 2)
    if password and email and role:
        user_dict = user.dict()
        hashed_password, salt = await utils.encrypt_password(user_dict.pop("password2"))
        user_dict.update({'password': hashed_password, 'salt': salt})
        try:
            await db.user_update(user_id, user_dict, session)
        except IntegrityError as err:
            error_detail = str(err.args).split('DETAIL:')[-1].strip()[:-4]
            raise HTTPException(status_code=500, detail=error_detail)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


async def delete_user(user_id, session):
    user = await UserRepository(session).get_one_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    await UserRepository(session).delete_one(user_id)
