from fastapi import HTTPException
from sqlalchemy import select, update, delete
from app.db.models import User


async def create_user(user, session):
    new_user = User(**user.dict())
    session.add(new_user)
    await session.commit()
    # return new_user


async def get_all_users(session):
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


async def get_user_by_id(user_id, session):
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    return result.scalars().first()


async def user_update(user_id, request_body, session):
    user = await session.execute(select(User).where(User.id == user_id))
    if user.first() is None:
        raise HTTPException(status_code=404, detail="User not found")
    stmt = update(User).where(User.id == user_id).values(**request_body.dict())
    await session.execute(stmt)
    await session.commit()


async def user_delete(user_id, session):
    user = await session.execute(select(User).where(User.id == user_id))
    if user.first() is None:
        raise HTTPException(status_code=404, detail="User not found")
    stmt = delete(User).where(User.id == user_id)
    await session.execute(stmt)
    await session.commit()