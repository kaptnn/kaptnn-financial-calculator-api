import enum
import uuid
from typing import Optional
from datetime import datetime
from sqlmodel import Field, Relationship, Column, Enum
from app.models.user_model import User
from app.models.base_model import BaseModel
from app.models.doc_category_model import DocumentCategory

class RequestStatus(str, enum.Enum):
    pending = "pending"
    uploaded = "uploaded"
    overdue = "overdue"

class DocumentRequest(BaseModel, table=True):
    __tablename__ = "document_requests"

    admin_id: uuid.UUID = Field(foreign_key="users.id")
    target_user_id: uuid.UUID = Field(foreign_key="users.id")
    category_id: uuid.UUID = Field(foreign_key="document_categories.id")
    due_date: datetime = Field()
    upload_date: Optional[datetime] = Field(default=None)
    status: RequestStatus = Field(sa_column=Column(Enum(RequestStatus)), default=RequestStatus.pending)

    admin: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "DocumentRequest.admin_id"})
    target_user: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "DocumentRequest.target_user_id"})
    category: Optional["DocumentCategory"] = Relationship()
