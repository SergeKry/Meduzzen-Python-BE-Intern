from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import companies as company_schema
import app.db.company as db_model
import app.db.user as db_model_user


class CompanyRepository:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = db_model.Company
        self.user_model = db_model_user.User

    async def create(self, company_details: company_schema.CompanyCreateRequest, user_id) -> db_model.Company:
        new_company = self.model(**company_details.dict(), owner_id=user_id)
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

    async def get_one_by_name(self, company_name) -> db_model.Company:
        query = select(self.model).where(self.model.name == company_name)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_one_by_id(self, company_id):
        query = select(self.model,
                       self.user_model).where(self.model.id == company_id).join(self.user_model,
                                                                              self.model.owner_id == self.user_model.id)
        query_result = await self.session.execute(query)
        return query_result.first()

    async def get_all(self):
        query = select(self.model, self.user_model).join(self.user_model, self.model.owner_id == self.user_model.id)
        query_result = await self.session.execute(query)
        return query_result.all()
