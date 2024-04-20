from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

import app.db.models as db_model


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_one(self, user) -> None:
        new_user = db_model.User(**user)
        self.session.add(new_user)
        await self.session.commit()

    async def get_all(self):
        query = select(db_model.User)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_by_id(self, user_id) -> db_model.User:
        query = select(db_model.User).where(db_model.User.id == user_id)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_one_by_username(self, username) -> db_model.User:
        query = select(db_model.User).where(db_model.User.username == username)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_one_by_email(self, email) -> db_model.User:
        query = select(db_model.User).where(db_model.User.email == email)
        result = await self.session.execute(query)
        return result.scalar()

#  user update needs to be improved and renamed to "update_one" after services/create_one_user is refactored
    async def update_one(self, user_id, new_values):
        stmt = update(db_model.User).where(db_model.User.id == user_id).values(**new_values)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_one(self, user_id):
        stmt = delete(db_model.User).where(db_model.User.id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()
