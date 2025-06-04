from sqlmodel import Field
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, DateTime, func
from app.models.base_model import BaseModel

class DocumentCategory(BaseModel, table=True):
    __tablename__ = "document_categories"

    name: str = Field(unique=True)
    
    created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), default=func.now()))
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))
