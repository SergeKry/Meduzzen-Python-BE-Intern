from datetime import datetime

from pydantic import BaseModel, Field


class CompanyDetails(BaseModel):
    id: int
    name: str
    details: str
    owner: str
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class CompanyCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    details: str = Field(max_length=300)


class CompanyCreateResponse(BaseModel):
    id: int
    name: str
    details: str
    owner: int

    class Config:
        orm_mode = True
        from_attributes = True
