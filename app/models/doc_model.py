import uuid
from typing import Optional
from datetime import datetime
from sqlmodel import Field, Relationship
from sqlalchemy import Column, DateTime, func
from app.models.user_model import User
from app.models.base_model import BaseModel
from app.models.company_model import Company
from app.models.doc_request_model import DocumentRequest


class Document(BaseModel, table=True):
    __tablename__ = "documents"

    request_id: Optional[uuid.UUID] = Field(default=None, foreign_key="document_requests.id")
    uploaded_by: uuid.UUID = Field(foreign_key="users.id")
    company_id: uuid.UUID = Field(foreign_key="companies.id")
    document_name: str = Field()
    document_path: str = Field()
    file_size: int = Field()
    mime_type: str = Field()

    created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), default=func.now()))
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))
    
    request: Optional["DocumentRequest"] = Relationship()
    uploader: Optional["User"] = Relationship()
    company: Optional["Company"] = Relationship()
