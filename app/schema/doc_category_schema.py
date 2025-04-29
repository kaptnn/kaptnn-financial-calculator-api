from uuid import UUID
from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel
from app.schema.base_schema import FindBase, ModelBaseInfo
from app.utils.schema import AllOptional

class BaseDocumentCategory(BaseModel):
    name: str

    class Config:
        from_attributes: True

class DocumentCategory(ModelBaseInfo, BaseDocumentCategory, metaclass=AllOptional):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes: True

class FindAllDocumentCategoriesResponse(BaseModel):
    message: str
    result: Optional[List[DocumentCategory]]
    meta: Optional[FindBase]
    
class FindDocumentCategoryByOptionsRequest(BaseModel):
    option: str
    value: Optional[Union[str, UUID]]

class FindDocumentCategoryByOptionsResponse(BaseModel):
    message: str
    result: Optional[DocumentCategory]
    meta: Optional[FindBase]

class CreateDocumentCategoryRequest(BaseModel):
    name: str

class CreateDocumentCategoryResponse(BaseModel):
    message: str
    result: Optional[DocumentCategory]
    meta: Optional[FindBase]

class UpdateDocumentCategoryRequest(BaseModel):
    name: Optional[str]

class UpdateDocumentCategoryResponse(BaseModel):
    message: str
    result: Optional[DocumentCategory]
    meta: Optional[FindBase]

class DeleteDocumentCategoryResponse(BaseModel):
    message: str
    result: Optional[DocumentCategory]
    meta: Optional[FindBase]