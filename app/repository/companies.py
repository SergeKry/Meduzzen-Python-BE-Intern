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
        new_company = self.model(**company_details.dict(), owner=self.user.id)
        self.session.add(new_company)
        await self.session.commit()
        return new_company
