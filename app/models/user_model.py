import uuid
from typing import Optional
from sqlmodel import Field, Relationship
from app.models.base_model import BaseModel
from app.models.profile_model import Profile
from app.models.company_model import Company

class User(BaseModel, table=True):
    __tablename__ = "users"

    name: str = Field()
    email: str = Field(index=True, unique=True)
    password: str = Field()
    company_id: Optional[uuid.UUID] = Field(default=None, foreign_key="companies.id")

    company: Optional["Company"] = Relationship(back_populates="users")
    profile: Optional["Profile"] = Relationship(back_populates="user")
