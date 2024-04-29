from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import BaseModel


class User(BaseModel):
    __tablename__: str = 'users'

    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(320), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(Integer, ForeignKey('roles.id'), nullable=False, default=2)


class Role(BaseModel):
    __tablename__ = 'roles'

    role_name = Column(String, unique=True, nullable=False)
