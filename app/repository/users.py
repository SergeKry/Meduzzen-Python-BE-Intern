from sqlalchemy import select, update, delete
import app.db.models as db_model


async def create_user(user, session) -> None:
    new_user = db_model.User(**user)
    session.add(new_user)
    await session.commit()


async def get_all_users(session) -> list:
    query = select(db_model.User)
    result = await session.execute(query)
    return result.scalars().all()


async def get_user_by_id(user_id, session) -> db_model.User:
    query = select(db_model.User).where(db_model.User.id == user_id)
    result = await session.execute(query)
    return result.scalar()


async def user_update(user_id, new_values, session):
    stmt = update(db_model.User).where(db_model.User.id == user_id).values(**new_values)
    await session.execute(stmt)
    await session.commit()


async def user_delete(user_id, session):
    stmt = delete(db_model.User).where(db_model.User.id == user_id)
    await session.execute(stmt)
    await session.commit()
