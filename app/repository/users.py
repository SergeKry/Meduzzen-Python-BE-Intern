from fastapi import HTTPException
from sqlalchemy import select, update, delete
from app.db.models import User


async def create_user(user, session):
    new_user = User(**user)
    session.add(new_user)
    await session.commit()


async def get_all_users(session):
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


async def get_user_by_id(user_id, session):
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    return result.scalar()


async def user_update(user_id, new_values, session):
    stmt = update(User).where(User.id == user_id).values(**new_values)
    await session.execute(stmt)
    await session.commit()


async def user_delete(user_id, session):
    stmt = delete(User).where(User.id == user_id)
    await session.execute(stmt)
    await session.commit()
