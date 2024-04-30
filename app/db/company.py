import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.database import BaseModel


class RequestType(enum.Enum):
    INVITATION = 'invitation'
    REQUEST = 'request'


class Status(enum.Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'


class RoleName(enum.Enum):
    OWNER = 'owner'
    ADMIN = 'admin'
    USER = 'user'


class Company(BaseModel):
    __tablename__ = 'companies'

    name = Column(String(100), nullable=False)
    details = Column(String(300))
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship("User")

    members = relationship("CompanyMember", back_populates='company')


class Action(BaseModel):
    __tablename__ = 'actions'

    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    request_type = Column(SQLEnum(RequestType), nullable=False)
    status = Column(SQLEnum(Status), nullable=False)


class CompanyMember(BaseModel):
    __tablename__ = 'company_members'

    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)

    company = relationship("Company", back_populates="members")
    user = relationship("User", back_populates="companies")


class CompanyRole(BaseModel):
    __tablename__ = 'company_roles'

    role_name = Column(SQLEnum(RoleName), nullable=False)
