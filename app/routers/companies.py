from fastapi import APIRouter
from starlette import status

from app.schemas import companies as schema
from app.routers.routers import db_dependency, user_dependency
from app.services.companies import CompanyService as Service

company_router = APIRouter(prefix="/company", tags=["Companies"])


@company_router.post("/", response_model=schema.CompanyCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_company(company_details: schema.CompanyCreateRequest, session: db_dependency, user: user_dependency):
    new_company = await Service(session, user).create_company(company_details)
    return new_company
