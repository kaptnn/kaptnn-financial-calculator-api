import enum
import uuid
from typing import Optional
from sqlmodel import Field, Relationship, Column, Enum
from app.models.user_model import User
from app.models.doc_model import Document
from app.models.base_model import BaseModel

class PermissionLevel(str, enum.Enum):
    read = "read"
    write = "write"
    admin = "admin"

class DocumentPermission(BaseModel, table=True):
    __tablename__ = "document_permissions"

    document_id: uuid.UUID = Field(foreign_key="documents.id")
    user_id: uuid.UUID = Field(foreign_key="users.id")
    permission: PermissionLevel = Field(sa_column=Column(Enum(PermissionLevel)), default=PermissionLevel.read)

    document: Optional["Document"] = Relationship()
    user: Optional["User"] = Relationship()
