import datetime
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, LargeBinary
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)


class User(BaseModel):
    __tablename__: str = 'users'

    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(320), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(Integer, ForeignKey('roles.id'), nullable=False, default=2)


class Role(BaseModel):
    __tablename__ = 'roles'

    role_name = Column(String, unique=True, nullable=False)


class Company(BaseModel):
    __tablename__ = 'companies'

    name = Column(String(100), nullable=False)
    details = Column(String(300))
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship("User")
