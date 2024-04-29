from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import BaseModel


class Company(BaseModel):
    __tablename__ = 'companies'

    name = Column(String(100), nullable=False)
    details = Column(String(300))
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship("User")
