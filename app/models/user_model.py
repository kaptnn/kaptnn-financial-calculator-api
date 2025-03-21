import uuid
from datetime import datetime
from sqlmodel import Field, Relationship
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Column, DateTime, func
from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.profile_model import Profile
    from app.models.company_model import Company

class User(BaseModel, table=True):
    __tablename__ = "users"

    name: str = Field()
    email: str = Field(index=True, unique=True)
    password: str = Field()
    company_id: Optional[uuid.UUID] = Field(default=None, foreign_key="companies.id")

    created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), default=func.now()))
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))

    company: Optional["Company"] = Relationship(back_populates="users")
    profile: Optional["Profile"] = Relationship(back_populates="user")
