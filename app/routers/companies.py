from fastapi import APIRouter, HTTPException
from starlette import status

from app.schemas import companies as schema
from app.routers.routers import db_dependency, user_dependency
from app.services.companies import CompanyService as Service

company_router = APIRouter(prefix="/company", tags=["Companies"])


@company_router.post("/", response_model=schema.CompanyCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_company(company_details: schema.CompanyCreateRequest, session: db_dependency, user: user_dependency):
    new_company = await Service(session, user).create_company(company_details)
    return new_company


@company_router.get("/")
async def get_all_companies(session: db_dependency, user: user_dependency) -> schema.CompanyListResponse:
    all_companies = await Service(session, user).get_all_companies()
    return all_companies


@company_router.get("/{company_id}")
async def get_company(company_id: int, session: db_dependency, user: user_dependency) -> schema.CompanyDetails:
    company = await Service(session, user).company_details_by_id(company_id)  # need to create this method in service and repository
    return company
