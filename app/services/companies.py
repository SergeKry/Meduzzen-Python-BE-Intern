from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.repository.companies import CompanyRepository
from app.schemas import users as user_schema
from app.schemas import companies as company_schema


class CompanyService:

    def __init__(self, session: AsyncSession, user: user_schema.User):
        self.session = session
        self.user = user
        self.repository = CompanyRepository(session, user)

    async def create_company(self, company_details: company_schema.CompanyCreateRequest):
        if await self.repository.get_one_by_name(company_details.name):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Such company already exists')
        new_company = await self.repository.create(company_details)
        return company_schema.CompanyCreateResponse.from_orm(new_company)
