import uuid
from datetime import datetime
from typing import Tuple, TypedDict, Optional, Union
from fastapi import HTTPException
from app.core.exceptions import InternalServerError
from app.models.doc_request_model import DocumentRequest
from app.services.base_service import BaseService
from app.repositories.docs_request_repo import DocsRequestRepository 
from app.schema.doc_request_schema import CreateDocumentReqRequest, CreateDocumentReqResponse, UpdateDocumentReqRequest, UpdateDocumentReqResponse, DeleteDocumentReqResponse, DocumentReq

class DocumentRequestDict(TypedDict):
    id: str
    admin_id: str
    target_user_id: str
    category_id: str
    due_date: datetime
    upload_date: Optional[datetime]
    status: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class DocsRequestService(BaseService):
    def __init__(self, docs_req_repository: DocsRequestRepository):
        self.docs_req_repository = docs_req_repository
        super().__init__(docs_req_repository)

    def get_all_docs_requests(self, page: int, limit: int, sort: str, order: str) -> dict:
        docs_reqs = self.docs_req_repository.get_all_docs_requests()

        if not docs_reqs:
            return {"result": [], "total_items": 0, "total_pages": 0}

        if sort not in docs_reqs[0]:
            raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort}")

        reverse = (order.lower() == "desc")
        companies_sorted = sorted(docs_reqs, key=lambda x: x.get(sort, ""), reverse=reverse)

        total_items = len(companies_sorted)
        total_pages = (total_items + limit - 1) // limit
        offset = (page - 1) * limit
        paginated_docs_reqs = companies_sorted[offset : offset + limit]

        return {
            "result": paginated_docs_reqs,
            "total_items": total_items,
            "total_pages": total_pages,
        }

    def get_docs_request_by_options(self, option: str, value: Union[str, uuid.UUID]) -> DocumentRequestDict:
        result = self.docs_req_repository.get_docs_request_by_options(option, value)

        if not result:
            raise HTTPException(status_code=404, detail="Company not found")
        
        return DocumentRequestDict(
            id=str(result.id),
            admin_id=str(result.admin_id),
            target_user_id=str(result.target_user_id),
            category_id=str(result.category_id),
            due_date=result.due_date,
            upload_date=result.upload_date,
            status=result.status,
            created_at=result.created_at,
            updated_at=result.updated_at,
        )

    def create_docs_request(self, admin_id: Union[str, uuid.UUID], docs_request: CreateDocumentReqRequest) -> CreateDocumentReqResponse:
        new_docs_request = self.docs_req_repository.create_docs_request(admin=admin_id, target_user=docs_request.target_user_id, category=docs_request.category_id, due_date=docs_request.due_date, upload_date=docs_request.upload_date)

        if not new_docs_request:
            raise InternalServerError("Failed to create document request. Please try again later")

        result = DocumentReq(
            id=str(new_docs_request.id),
            admin_id=str(new_docs_request.admin_id),
            target_user_id=str(new_docs_request.target_user_id),
            category_id=str(new_docs_request.category_id),
            due_date=new_docs_request.due_date,
            upload_date=new_docs_request.upload_date,
            status=new_docs_request.status,
            created_at=new_docs_request.created_at,
            updated_at=new_docs_request.updated_at,
        )

        return CreateDocumentReqResponse(
            message="Document request successfully registered", 
            result=result.model_dump()
        )

    def update_docs_request(self, docs_request_id: str, docs_request: UpdateDocumentReqRequest) -> UpdateDocumentReqResponse:
        existing_docs_request = self.docs_req_repository.get_docs_request_by_options("id", docs_request_id)
        
        if not existing_docs_request:
            raise HTTPException(status_code=404, detail="Docs Request not found")

        updated_docs_request = self.docs_req_repository.update_docs_request(docs_request_id, docs_request)

        return DocumentRequest(
            id=updated_docs_request._id,
            admin_id=updated_docs_request.admin_id,
            target_user_id=str(updated_docs_request.target_user_id),
            category_id=str(updated_docs_request.category_id),
            due_date=updated_docs_request.due_date,
            upload_date=updated_docs_request.upload_date,
            status=updated_docs_request.status,
            created_at=updated_docs_request.created_at,
            updated_at=updated_docs_request.updated_at,
        )

    def delete_docs_request(self, docs_request_id: str) -> DeleteDocumentReqResponse:
        existing_docs_request = self.docs_req_repository.get_docs_request_by_options("id", docs_request_id)
        if not existing_docs_request:
            raise HTTPException(status_code=404, detail="User not found")

        success = self.docs_req_repository.delete_docs_request(docs_request_id)
        if not success:
            raise InternalServerError("Failed to delete document request. Please try again later")
        
        return {"message": "Docs request deleted successfully"}
