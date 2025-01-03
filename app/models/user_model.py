from typing import Optional
from sqlmodel import Field, Relationship, DateTime, Column, func
from datetime import datetime
from app.models.base_model import BaseModel
from sqlalchemy import Column

class User(BaseModel, table=True):
    __tablename__: str = "users"

    name: str = Field()
    email: str = Field(index=True, unique=True)
    password: str = Field()
    profile: Optional["Profile"] = Relationship(back_populates="user")

    created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), default=func.now()))
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))

from app.models.profile_model import Profile
Profile.model_rebuild()