from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status

from app.schemas import users as user_schema
from app.utils import utils
from app.repository import users as db


async def user_details(query_result):
    user = user_schema.UserDetailResponse(id=query_result.id,
                                          username=query_result.username,
                                          email=query_result.email,
                                          role=query_result.role)
    return user


async def get_all_users(query_result):
    result = []
    for item in query_result:
        user = await user_details(item)
        result.append(user)
    return {'users': result}


async def add_user(user, session):
    user_dict = user.dict()
    password = user_dict['password'] == user_dict['password2']
    email = utils.validate_email(user_dict['email'])
    role = user_dict['role'] in (0, 1, 2)
    if password and email and role:
        user_dict = user.dict()
        hashed_password, salt = await utils.encrypt_password(user_dict.pop("password2"))
        user_dict.update({'password': hashed_password, 'salt': salt})
        try:
            await db.create_user(user_dict, session)
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