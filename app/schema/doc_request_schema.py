from uuid import UUID
from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel
from app.models.doc_request_model import RequestStatus
from app.schema.base_schema import FindBase, ModelBaseInfo
from app.utils.schema import AllOptional

class BaseDocumentReq(BaseModel):
    request_title: str
    request_desc: str
    admin_id: UUID
    target_user_id: UUID
    category_id: UUID
    due_date: datetime
    upload_date: Optional[datetime]
    status: RequestStatus

    class Config:
        from_attributes: True

class DocumentReq(ModelBaseInfo, BaseDocumentReq, metaclass=AllOptional):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes: True

class FindAllDocumentReqsResponse(BaseModel):
    message: str
    result: Optional[List[DocumentReq]]
    meta: Optional[FindBase]

class FindDocumentReqByOptionsRequest(BaseModel):
    option: str
    value: Optional[Union[str, UUID]]

class FindDocumentReqByOptionsResponse(BaseModel):
    message: str
    result: Optional[DocumentReq]
    meta: Optional[FindBase]

class CreateDocumentReqRequest(BaseModel):
    request_title: str
    request_desc: str
    target_user_id: UUID
    category_id: UUID
    due_date: datetime

class CreateDocumentReqResponse(BaseModel):
    message: str
    result: Optional[DocumentReq]
    meta: Optional[FindBase]

class UpdateDocumentReqRequest(BaseModel):
    request_title: Optional[str]
    request_desc: Optional[str]
    target_user_id: Optional[UUID]
    category_id: Optional[UUID]
    due_date: Optional[datetime]
    upload_date: Optional[datetime]
    status: Optional[RequestStatus]

class UpdateDocumentReqResponse(BaseModel):
    message: str
    result: Optional[DocumentReq]  
    meta: Optional[FindBase]

class DeleteDocumentReqResponse(BaseModel):
    message: str
    result: Optional[DocumentReq]  
    meta: Optional[FindBase]