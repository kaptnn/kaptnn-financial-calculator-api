from typing import Any, Dict, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from dependency_injector.wiring import Provide
from app.core.container import Container
from app.core.middleware import inject
from app.core.dependencies import get_current_user
from app.models.doc_request_model import RequestStatus
from app.models.profile_model import Role
from app.schema.doc_request_schema import FindDocumentReqByOptionsResponse, CreateDocumentReqRequest, CreateDocumentReqResponse, UpdateDocumentReqRequest, UpdateDocumentReqResponse, DeleteDocumentReqResponse, FindAllDocumentReqsResponse
from app.schema.user_schema import User
from app.services.docs_manager.docs_request_service import DocsRequestService

router = APIRouter(prefix="/document-requests", tags=["Document Request"])

@router.get("/", 
    response_model=FindAllDocumentReqsResponse, 
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True)
@inject
def get_all_docs_requests(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of users per page"),
    sort: str = Query("created_at", description="Field to sort by"),
    order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order (asc or desc)"),
    status: Optional[RequestStatus] = Query(None),
    admin_id: Optional[UUID] = Query(None),
    target_user_id: Optional[UUID] = Query(None),
    category_id: Optional[UUID] = Query(None),
    name: Optional[str] = Query(None, description="Filter by name substring"),
    service: DocsRequestService = Depends(Provide[Container.docs_request_service]),
    current_user: User = Depends(get_current_user),
):
    filters: Dict[str, Any] = {}
    if status:
        filters["status"] = status
    if admin_id:
        filters["admin_id"] = admin_id
    if target_user_id:
        filters["target_user_id"] = target_user_id
    if category_id:
        filters["category_id"] = category_id
    if name:
        filters["name"] = name
        
    docs_requests = service.get_all_docs_requests(
        page=page, 
        limit=limit, 
        sort=sort, 
        order=order,
        filters=filters
    )

    return {
        "message": "Document categories retrieved successfully",
        "result": docs_requests.result,
        "meta": {
            "current_page": page,
            "total_pages": docs_requests.meta.total_pages,
            "total_items": docs_requests.meta.total_items,
        },
    }

@router.get("/summary", status_code=status.HTTP_200_OK)
@inject
def get_all_docs_requests(
    service: DocsRequestService = Depends(Provide[Container.docs_request_service]),
    current_user: User = Depends(get_current_user),
):
    summary = service.get_doc_request_category_summary()

    return {
        "message": "Document summary retrieved successfully",
        "result": summary,
        "meta": None,
    }

@router.get("/summary/status", status_code=status.HTTP_200_OK)
@inject
def get_all_docs_requests(
    service: DocsRequestService = Depends(Provide[Container.docs_request_service]),
    current_user: User = Depends(get_current_user),
):
    summary_status = service.get_doc_status_count()

    return {
        "message": "Document summary retrieved successfully",
        "result": summary_status,
        "meta": None,
    }

@router.get("/{docs_request_id}", 
    response_model=FindDocumentReqByOptionsResponse, 
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True)
@inject
def get_docs_request_by_id(
    docs_request_id: UUID,
    service: DocsRequestService = Depends(Provide[Container.docs_request_service]),
    current_user: User = Depends(get_current_user),
):
    docs_request = service.get_docs_request_by_options("id", docs_request_id)
    return FindDocumentReqByOptionsResponse(
        message="Docs request retrieved successfully",
        result=docs_request.result,
        meta=None
    )

@router.post("/", 
    response_model=CreateDocumentReqResponse, 
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True)
@inject
def create_docs_request(
    docs_request: CreateDocumentReqRequest,
    service: DocsRequestService = Depends(Provide[Container.docs_request_service]),
    current_user: User = Depends(get_current_user),
):
    return service.create_docs_request(current_user, docs_request)

@router.put("/{docs_request_id}", 
    response_model=UpdateDocumentReqResponse, 
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True)
@inject
def update_docs_request(
    docs_request_id: UUID,
    docs_request_info: UpdateDocumentReqRequest,
    service: DocsRequestService = Depends(Provide[Container.docs_request_service]),
    current_user: User = Depends(get_current_user),
):
    docs_request = service.update_docs_request(docs_request_id, docs_request_info)
    return FindDocumentReqByOptionsResponse(
        message="Document request updated successfully",
        result=docs_request.result,
        meta=None
    )

@router.delete("/{docs_request_id}", 
    response_model=DeleteDocumentReqResponse, 
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True)
@inject
def delete_docs_request(
    docs_request_id: UUID,
    service: DocsRequestService = Depends(Provide[Container.docs_request_service]),
    current_user: User = Depends(get_current_user),
):
    service.delete_docs_request(docs_request_id)
    return DeleteDocumentReqResponse(
        message='Document request deleted successfully',
        result=None,
        meta=None
    )