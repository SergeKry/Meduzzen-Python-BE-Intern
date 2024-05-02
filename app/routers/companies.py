from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status
from app.schemas import companies as schema
from app.routers.routers import db_dependency, user_dependency, token_dependency
from app.services.companies import CompanyService as Service

token_auth_scheme = HTTPBearer()

company_router = APIRouter(prefix="/company", tags=["Companies"])


@company_router.post("/", response_model=schema.CompanyCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_company(company_details: schema.CompanyCreateRequest, session: db_dependency, user: user_dependency):
    new_company = await Service(session).create_company(company_details, user)
    return new_company


@company_router.get("/", response_model=schema.CompanyListResponse, status_code=status.HTTP_200_OK)
async def get_all_companies(session: db_dependency, user: user_dependency):
    if user:
        all_companies = await Service(session).get_all_companies()
        return all_companies


@company_router.get("/{company_id}")
async def get_company(company_id: int,
                      session: db_dependency,
                      token: token_dependency) -> schema.CompanyDetails:
    company = await Service(session, token).company_details_by_id(company_id)
    return company


@company_router.patch("/{company_id}")
async def update_company(company_id: int, request_body: schema.CompanyUpdateRequest,
                         session: db_dependency,
                         token: token_dependency) -> schema.CompanyDetails:
    await Service(session, token).update_company(company_id, request_body)
    return await Service(session, token).company_details_by_id(company_id)


@company_router.delete("/{company_id}")
async def delete_company(company_id: int,
                         session: db_dependency,
                         token: token_dependency) -> str:
    await Service(session, token).delete_company(company_id)
    return 'Company deleted'
