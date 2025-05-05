from uuid import UUID
from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel
from app.schema.base_schema import FindBase, ModelBaseInfo
from app.utils.schema import AllOptional

class BaseDocument(BaseModel):
    request_id: UUID
    uploaded_by: UUID
    company_id: UUID
    document_name: str 
    document_path: str 
    file_size: int 
    mime_type: str  

    class Config:
        from_attributes: True

class Document(ModelBaseInfo, BaseDocument, metaclass=AllOptional): 
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes: True

class FindAllDocumentsResponse(BaseModel):
    message: str
    result: Optional[List[Document]]
    meta: Optional[FindBase]

class FindDocumentByOptionsRequest(BaseModel):
    option: str
    value: Optional[Union[str, UUID]]

class FindDocumentByOptionsResponse(BaseModel):
    message: str
    result: Optional[Document]
    meta: Optional[FindBase]

class CreateDocumentRequest(BaseModel):
    document_name: str 
    request_id: UUID

class CreateDocumentResponse(BaseModel):
    message: str
    result: Optional[Document]
    meta: Optional[FindBase]

class UpdateDocumentRequest(BaseModel):
    document_name: str   

class UpdateDocumentResponse(BaseModel):
    message: str
    result: Optional[Document]  
    meta: Optional[FindBase]

class DeleteDocumentResponse(BaseModel):
    message: str
    result: Optional[Document]
    meta: Optional[FindBase]