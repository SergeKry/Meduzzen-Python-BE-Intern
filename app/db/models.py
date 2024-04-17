import datetime
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))


class User(BaseModel):
    __tablename__: str = 'users'

    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(320), unique=True, nullable=False)
    password = Column(String(127), nullable=False)
    role = Column(Integer, ForeignKey('roles.id'), nullable=False, default=1)


class Role(BaseModel):
    __tablename__ = 'roles'

    role_name = Column(String, unique=True, nullable=False)
