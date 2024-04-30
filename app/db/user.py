from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import BaseModel
from app.db.company import CompanyMember


class User(BaseModel):
    __tablename__: str = 'users'

    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(320), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(Integer, ForeignKey('roles.id'), nullable=False, default=2)

    companies = relationship('CompanyMember', back_populates='user')


class Role(BaseModel):
    __tablename__ = 'roles'

    role_name = Column(String, unique=True, nullable=False)
