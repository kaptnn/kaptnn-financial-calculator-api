import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.models.doc_request_model import RequestStatus
from app.schema.base_schema import ModelBaseInfo
from app.utils.schema import AllOptional

class BaseDocumentReq(BaseModel):
    admin_id: str
    target_user_id: str
    category_id: str
    due_date: datetime
    upload_date: Optional[datetime]
    status: RequestStatus
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class DocumentReq(ModelBaseInfo, BaseDocumentReq, metaclass=AllOptional): ...

class FindAllDocumentReqsResponse(BaseModel):
    message: str
    result: Optional[List[DocumentReq]]

class FindDocumentReqByOptionsRequest(BaseModel):
    option: str
    value: str | int | uuid.UUID

class FindDocumentReqByOptionsResponse(BaseModel):
    message: str
    result: Optional[DocumentReq]

class CreateDocumentReqRequest(BaseModel):
    request_title: str
    request_desc: str
    target_user_id: str
    category_id: str
    due_date: datetime
    updated_date: Optional[datetime]

class CreateDocumentReqResponse(BaseModel):
    message: str
    result: DocumentReq

class UpdateDocumentReqRequest(BaseModel):
    request_title: Optional[str]
    request_desc: Optional[str]
    target_user_id: Optional[str]
    category_id: Optional[str]
    due_date: Optional[datetime]
    upload_date: Optional[datetime]
    status: Optional[RequestStatus]

class UpdateDocumentReqResponse(BaseModel):
    message: str
    result: Optional[DocumentReq]  

class DeleteDocumentReqResponse(BaseModel):
    message: str