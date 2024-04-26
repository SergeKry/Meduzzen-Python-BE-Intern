from typing import List

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import users as user_schema
from app.schemas import companies as company_schema
import app.db.models as db_model


class CompanyRepository:

    def __init__(self, session: AsyncSession, user: user_schema.User):
        self.session = session
        self.user = user
        self.model = db_model.Company

    async def create(self, company_details: company_schema.CompanyCreateRequest) -> db_model.Company:
        new_company = self.model(**company_details.dict(), owner_id=self.user.id)
        self.session.add(new_company)
        await self.session.commit()
        return new_company

    async def update(self, company_id, request_body: dict) -> None:
        stmt = update(self.model).where(self.model.id == company_id).values(**request_body)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, company_id) -> None:
        stmt = delete(self.model).where(self.model.id == company_id)
        await self.session.execute(stmt)
        await self.session.commit()

    @staticmethod
    async def unpack_company_details(result) -> dict:
        if result:
            company = result[0]
            user = result[1]
            filtered_result = {'id': company.id,
                               'name': company.name,
                               'details': company.details,
                               'owner': user.username,
                               'created_at': company.created_at}
            return filtered_result

    async def get_one_by_name(self, company_name) -> db_model.Company:
        query = select(self.model).where(self.model.name == company_name)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_one_by_id(self, company_id) -> dict:
        query = select(self.model,
                       db_model.User).where(self.model.id == company_id).join(db_model.User,
                                                                              self.model.owner_id == db_model.User.id)
        query_result = await self.session.execute(query)
        result = await self.unpack_company_details(query_result.first())
        return result

    async def get_all(self) -> List[dict]:
        query = select(self.model, db_model.User).join(db_model.User, self.model.owner_id == db_model.User.id)
        query_result = await self.session.execute(query)
        result = [await self.unpack_company_details(row) for row in query_result.all()]
        return result
