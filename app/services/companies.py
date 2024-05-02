from fastapi import HTTPException
from fastapi.security import HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.repository.companies import CompanyRepository
from app.repository.actions import ActionsRepository
from app.schemas import users as user_schema
from app.schemas import companies as company_schema
from app.utils.utils import decode_access_token

token_auth_scheme = HTTPBearer()


class CompanyService:

    def __init__(self, session: AsyncSession, token=None):
        self.session = session
        self.token = token
        self.repository = CompanyRepository(session)

    async def create_company(self, company_details: company_schema.CompanyCreateRequest,
                             user: user_schema.User) -> company_schema.CompanyCreateResponse:
        if await self.repository.get_one_by_name(company_details.name):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Such company already exists')
        #  Creating Company
        new_company = await self.repository.create(company_details, user.id)
        #  Adding owner as company member with OWNER role
        await ActionsRepository(self.session).add_member(new_company.id, user.id, role_id=1)
        return company_schema.CompanyCreateResponse.from_orm(new_company)

    async def get_company_details(self, company_id: int):
        result = await self.repository.get_one_by_id(company_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Company not found')
        company = company_schema.Company.from_orm(result[0])
        user = user_schema.User.from_orm(result[1])
        return company, user

    async def validate_owner_permissions(self, user: user_schema.User) -> bool:
        try:
            token_user_id, token_email, token_username = decode_access_token(self.token.credentials)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token invalid')
        if token_email != user.email:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Wrong permissions')
        return True

    async def update_company(self, company_id, request_body) -> None:
        company, user = await self.get_company_details(company_id)
        if await self.validate_owner_permissions(user):
            new_values_dict = request_body.dict(exclude_unset=True)
            await self.repository.update(company_id, new_values_dict)

    async def delete_company(self, company_id) -> None:
        company, user = await self.get_company_details(company_id)
        if await self.validate_owner_permissions(user):
            await self.repository.delete(company_id)

    async def get_all_companies(self) -> dict:
        companies = await self.repository.get_all()
        companies_list = [company_schema.CompanyDetails(id=company[0].id,
                                                        name=company[0].name,
                                                        details=company[0].details,
                                                        owner=company[1].username,
                                                        created_at=company[0].created_at) for company in companies]
        return {'companies': companies_list}

    async def company_details_by_id(self, company_id: int) -> company_schema.CompanyDetails:
        company, user = await self.get_company_details(company_id)
        company_details = company_schema.CompanyDetails(id=company.id, name=company.name, details=company.details,
                                                        owner=user.username, created_at=company.created_at)
        return company_details
