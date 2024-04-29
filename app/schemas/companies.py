from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class Company(BaseModel):
    id: int
    name: str
    details: str
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class CompanyDetails(BaseModel):
    id: int
    name: str
    details: str
    owner: str
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class CompanyListResponse(BaseModel):
    companies: List[CompanyDetails]

    class Config:
        orm_mode = True
        from_attributes = True


class CompanyCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    details: str = Field(max_length=300)


class CompanyUpdateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100, default=None)
    details: str = Field(max_length=300, default=None)


class CompanyCreateResponse(BaseModel):
    id: int
    name: str
    details: str

    class Config:
        orm_mode = True
        from_attributes = True
