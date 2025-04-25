import uuid
from fastapi import APIRouter, Depends, Query, status
from dependency_injector.wiring import Provide
from app.core.container import Container
from app.core.middleware import inject
from app.core.dependencies import get_current_user
from app.services.user_service import UserDict
from app.schema.doc_request_schema import FindDocumentReqByOptionsResponse, CreateDocumentReqRequest, CreateDocumentReqResponse, UpdateDocumentReqRequest, UpdateDocumentReqResponse, DeleteDocumentReqResponse
from app.services.docs_manager.docs_request_service import DocsRequestService

router = APIRouter(prefix="/docs-request", tags=["docs requests"])

@router.get("/", response_model=dict, status_code=status.HTTP_200_OK)
@inject
def get_all_docs_requests(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(5, ge=1, le=100, description="Number of users per page"),
    sort: str = Query("created_at", description="Field to sort by"),
    order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order (asc or desc)"),
    service: DocsRequestService = Depends(Provide[Container.docs_request_service]),
    current_user: UserDict = Depends(get_current_user),
):
    docs_requests = service.get_all_docs_requests(page=page, limit=limit, sort=sort, order=order)
    return {
        "message": "Docs categories retrieved successfully",
        "result": docs_requests["result"],
        "pagination": {
            "current_page": page,
            "total_pages": docs_requests["total_pages"],
            "total_items": docs_requests["total_items"],
        },
    }

@router.get("/{docs_request_id}", response_model=FindDocumentReqByOptionsResponse, status_code=status.HTTP_200_OK)
@inject
def get_docs_request_by_id(
    docs_request_id: uuid.UUID,
    service: DocsRequestService = Depends(Provide[Container.docs_request_service]),
    current_user: UserDict = Depends(get_current_user),
):
    result = service.get_docs_request_by_options(option="id", value=docs_request_id)
    return {
        "message": "Docs request retrieved successfully",
        "result": result,
    }

@router.post("/", response_model=CreateDocumentReqResponse, status_code=status.HTTP_201_CREATED)
@inject
def create_docs_request(
    docs_request: CreateDocumentReqRequest,
    service: DocsRequestService = Depends(Provide[Container.docs_request_service]),
    current_user: UserDict = Depends(get_current_user),
):
    
    return service.create_docs_request(current_user["id"], docs_request)

@router.put("/{docs_request_id}", response_model=UpdateDocumentReqResponse, status_code=status.HTTP_200_OK)
@inject
def update_docs_request(
    docs_request: UpdateDocumentReqRequest,
    service: DocsRequestService = Depends(Provide[Container.docs_request_service]),
    current_user: UserDict = Depends(get_current_user),
):
    result = service.update_docs_request(docs_request)
    return {
        "message": "Docs request updated successfully",
        "result": result,
    }

@router.delete("/{docs_request_id}", response_model=DeleteDocumentReqResponse, status_code=status.HTTP_200_OK)
@inject
def delete_docs_request(
    docs_request_id: uuid.UUID,
    service: DocsRequestService = Depends(Provide[Container.docs_request_service]),
    current_user: UserDict = Depends(get_current_user),
):
    return service.delete_docs_request(docs_request_id)