import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.schema.base_schema import ModelBaseInfo
from app.utils.schema import AllOptional

class BaseDocument(BaseModel):
    request_id: str
    uploaded_by: str
    company_id: str
    document_name: str 
    document_path: str 
    file_size: int 
    mime_type: str  
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class Document(ModelBaseInfo, BaseDocument, metaclass=AllOptional): ...

class FindAllDocumentsResponse(BaseModel):
    message: str
    result: Optional[List[Document]]

class FindDocumentByOptionsRequest(BaseModel):
    option: str
    value: str | int | uuid.UUID

class FindDocumentByOptionsResponse(BaseModel):
    message: str
    result: Optional[Document]

class CreateDocumentRequest(BaseModel):
    document_name: str 

class CreateDocumentResponse(BaseModel):
    message: str
    result: Document

class UpdateDocumentRequest(BaseModel):
    document_name: str   

class UpdateDocumentResponse(BaseModel):
    message: str
    result: Optional[Document]  

class DeleteDocumentResponse(BaseModel):
    message: str