from typing import Sequence

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
import app.db.models as db_model


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = db_model.User

    async def create_one(self, user) -> db_model.User:
        new_user = self.model(**user)
        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def get_all(self) -> Sequence[db_model.User]:
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_by_id(self, user_id) -> db_model.User:
        query = select(self.model).where(self.model.id == user_id)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_one_by_username(self, username) -> db_model.User:
        query = select(self.model).where(self.model.username == username)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_one_by_email(self, email) -> db_model.User:
        query = select(self.model).where(self.model.email == email)
        result = await self.session.execute(query)
        return result.scalar()

    async def update_one(self, user_id, new_values) -> None:
        stmt = update(self.model).where(self.model.id == user_id).values(**new_values)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_one(self, user_id) -> None:
        stmt = delete(self.model).where(self.model.id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()
