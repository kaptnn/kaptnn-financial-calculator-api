from sqlmodel import Field
from app.models.base_model import BaseModel

class DocumentCategory(BaseModel, table=True):
    __tablename__ = "document_categories"

    name: str = Field(unique=True)
