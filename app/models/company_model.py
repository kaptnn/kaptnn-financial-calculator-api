from typing import List
from sqlmodel import Field, Relationship
from app.models.user_model import User
from app.models.base_model import BaseModel

class Company(BaseModel, table=True):
    __tablename__ = "companies"

    company_name: str = Field(unique=True)

    users: List["User"] = Relationship(back_populates="company")
