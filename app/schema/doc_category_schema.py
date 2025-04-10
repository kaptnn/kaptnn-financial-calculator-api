import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.schema.base_schema import ModelBaseInfo
from app.utils.schema import AllOptional

class BaseDocumentCategory(BaseModel):
    name: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class DocumentCategory(ModelBaseInfo, BaseDocumentCategory, metaclass=AllOptional): ...

class FindAllDocumentCategoriesResponse(BaseModel):
    message: str
    result: Optional[List[DocumentCategory]]

class FindDocumentCategoryByOptionsRequest(BaseModel):
    option: str
    value: str | uuid.UUID

class FindDocumentCategoryByOptionsResponse(BaseModel):
    message: str
    result: Optional[DocumentCategory]

class CreateDocumentCategoryRequest(BaseModel):
    name: str

class CreateDocumentCategoryResponse(BaseModel):
    message: str
    result: DocumentCategory

class UpdateDocumentCategoryRequest(BaseModel):
    name: Optional[str]

class UpdateDocumentCategoryResponse(BaseModel):
    message: str
    result: Optional[DocumentCategory]  

class DeleteDocumentCategoryResponse(BaseModel):
    message: str