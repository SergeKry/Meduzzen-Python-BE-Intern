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

    async def create_company(self, company_details: company_schema.CompanyCreateRequest) -> company_schema.CompanyCreateResponse:
        if await self.repository.get_one_by_name(company_details.name):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Such company already exists')
        new_company = await self.repository.create(company_details)
        return company_schema.CompanyCreateResponse.from_orm(new_company)

    async def update_company(self, company_id, request_body) -> None:
        company = await self.repository.get_one_by_id(company_id)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Company not found')
        if company['owner'] != self.user.username:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Don't have permission to update company")
        new_values_dict = request_body.dict(exclude_unset=True)
        await self.repository.update(company_id, new_values_dict)

    async def get_all_companies(self) -> company_schema.CompanyListResponse:
        companies = await self.repository.get_all()
        return company_schema.CompanyListResponse(companies=companies)

    async def company_details_by_id(self, company_id: int):
        company = await self.repository.get_one_by_id(company_id)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Company not found')
        return company_schema.CompanyDetails(**company)
