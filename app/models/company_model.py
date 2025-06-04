from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship
from sqlalchemy import Column, DateTime, func
from app.models.user_model import User
from app.models.base_model import BaseModel

class Company(BaseModel, table=True):
    __tablename__ = "companies"

    company_name: str = Field(unique=True)
    year_of_assignment: int = Field()
    start_audit_period: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    end_audit_period: datetime = Field(sa_column=Column(DateTime(timezone=True)))

    created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), default=func.now()))
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))
    
    users: List["User"] = Relationship(back_populates="company")
