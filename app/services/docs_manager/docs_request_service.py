from datetime import datetime, timezone
from uuid import UUID
from typing import Any, Dict, Optional, Union
from fastapi import HTTPException, status
from app.core.exceptions import InternalServerError
from app.models.profile_model import Role
from app.models.doc_request_model import RequestStatus
from app.schema.user_schema import User
from app.services.base_service import BaseService
from app.repositories.docs_request_repo import DocsRequestRepository 
from app.repositories.user_repo import UserRepository
from app.schema.doc_request_schema import CreateDocumentReqRequest, CreateDocumentReqResponse, UpdateDocumentReqRequest, UpdateDocumentReqResponse, DeleteDocumentReqResponse, FindAllDocumentReqsResponse, FindDocumentReqByOptionsResponse

class DocsRequestService(BaseService):
    ALLOWED_SORTS = {"id", "request_title", "created_at", "admin_id", "target_user_id", "category_id", "due_date", "upload_date"}
    ALLOWED_ORDERS = {"asc", "desc"}
    ALLOWED_FILTERS = {"id", "status", "name", "admin_id", "target_user_id", "category_id"}

    def __init__(self, docs_req_repository: DocsRequestRepository, user_repository: UserRepository):
        self.docs_req_repository = docs_req_repository
        self.user_repository = user_repository
        super().__init__(docs_req_repository)
        super().__init__(user_repository)

    def get_all_docs_requests(
        self, 
        page: int = 1, 
        limit: int = 100, 
        sort: str = "created_at", 
        order: str = "asc",
        filters: Optional[Dict[str, Any]] = None
    ) -> FindAllDocumentReqsResponse:
        if page < 1:
            page = 1
        if not (1 <= limit <= 100):
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
        
        if sort not in self.ALLOWED_SORTS:
            raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort!r}. Must be one of {self.ALLOWED_SORTS}")
        
        order = order.lower()
        if order not in self.ALLOWED_ORDERS:
            raise HTTPException(status_code=400, detail=f"Invalid order: {order!r}. Must be one of {self.ALLOWED_ORDERS}")
        
        if filters is not None:
            invalid_keys = set(filters.keys()) - self.ALLOWED_FILTERS
            if invalid_keys:
                raise HTTPException(status_code=400, detail=f"Invalid filter keys: {invalid_keys}. Allowed filters are {self.ALLOWED_FILTERS}")

        return self.docs_req_repository.get_all_docs_requests(
            page=page,
            limit=limit,
            sort=sort,
            order=order,
            filters=filters
        )

    def get_docs_request_by_options(
        self, 
        option: str, 
        value: Union[str, UUID]
    ) -> FindDocumentReqByOptionsResponse:
        if option not in self.ALLOWED_FILTERS:
            raise HTTPException(status_code=400, detail="Invalid option field")

        response = self.docs_req_repository.get_docs_request_by_options(option, value)

        if response.result is None:
            raise HTTPException(status_code=404, detail="Company not found")
        
        return response

    def create_docs_request(self, admin: User, docs_request: CreateDocumentReqRequest) -> CreateDocumentReqResponse:
        if admin.profile.role != Role.admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is not authorized to create document requests."
            )
        
        existing_user = self.user_repository.get_user_by_options("id", admin.id)
        if existing_user is None:
            raise InternalServerError("User not found. Cannot create document request.")
        
        target_user = self.user_repository.get_user_by_options("id", docs_request.target_user_id)
        if target_user is None:
            raise InternalServerError("User not found. Cannot create document request.")

        current_time = datetime.now(timezone.utc)
        if docs_request.due_date < current_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Due date cannot be in the past."
            )

        new_docs_request = self.docs_req_repository.create_docs_request(
            request_title=docs_request.request_title,
            request_desc=docs_request.request_desc,
            admin=admin.id,
            target_user=docs_request.target_user_id,
            category=docs_request.category_id,
            due_date=docs_request.due_date
        )

        if not new_docs_request:
            raise InternalServerError("Failed to create document request. Please try again later")

        return CreateDocumentReqResponse(
            message="Document request successfully registered",
            result=None,
            meta=None
        )

    def update_docs_request(self, docs_request_id: UUID, docs_request_info: UpdateDocumentReqRequest) -> UpdateDocumentReqResponse:
        existing_docs_request = self.docs_req_repository.get_docs_request_by_options("id", docs_request_id)
        
        if existing_docs_request.result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document request not found")
        
        target_user = self.user_repository.get_user_by_options("id", docs_request_info.target_user_id)
        if target_user is None:
            raise InternalServerError("User not found. Cannot create document request.")
        
        response = self.docs_req_repository.update_docs_request(docs_request_id, docs_request_info)

        if not response:
            raise InternalServerError("Failed to update user. Please try again later")

        return response

    def delete_docs_request(self, docs_request_id: UUID) -> DeleteDocumentReqResponse:
        existing_docs_request = self.docs_req_repository.get_docs_request_by_options("id", docs_request_id)
        if not existing_docs_request:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document request not found")

        response = self.docs_req_repository.delete_docs_request(docs_request_id)
        if not response:
            raise InternalServerError("Failed to delete document request. Please try again later")
        
        return response


    def get_doc_request_category_summary(self):
        return self.docs_req_repository.doc_request_category_summary()
    
    def get_doc_status_count(self):
        return self.docs_req_repository.doc_status_count()