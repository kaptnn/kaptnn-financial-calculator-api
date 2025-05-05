from typing import Any, Dict, Optional
from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, Query, Request, UploadFile, status
from dependency_injector.wiring import Provide
from app.core.container import Container
from app.core.middleware import inject
from app.core.dependencies import get_current_user
from app.schema.doc_schema import CreateDocumentRequest, CreateDocumentResponse, DeleteDocumentResponse, FindAllDocumentsResponse, FindDocumentByOptionsResponse, UpdateDocumentRequest, UpdateDocumentResponse
from app.schema.user_schema import User
from app.services.docs_manager.docs_service import DocsService

router = APIRouter(prefix="/documents", tags=["Document Management"])

@router.get("/", 
    response_model=FindAllDocumentsResponse,
    status_code=status.HTTP_200_OK,
    response_model_exclude=None
)
@inject
def get_all_docs(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(5, ge=1, le=100, description="Number of users per page"),
    sort: str = Query("created_at", description="Field to sort by"),
    order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order (asc or desc)"),
    service: DocsService = Depends(Provide[Container.docs_service]),
    name: Optional[str] = Query(None, description="Filter by name substring"),
    current_user: User = Depends(get_current_user),
):
    filters: Dict[str, Any] = {}
    if name:
        filters["name"] = name
        
    docs = service.get_all_docs(
                page=page, 
                limit=limit, 
                sort=sort, 
                order=order,
                filters=filters
            )
    
    return {
        "message": "Documents retrieved successfully",
        "result": docs.result,
        "meta": {
            "current_page": page,
            "total_pages": docs.meta.total_pages,
            "total_items": docs.meta.total_items,
        },
    }

@router.get("/{docs_id}",
    response_model=FindDocumentByOptionsResponse,
    status_code=status.HTTP_200_OK,
    response_model_exclude=None
)
@inject
def get_docs_by_id(
    docs_id: UUID,
    service: DocsService = Depends(Provide[Container.docs_service]),
    current_user: User = Depends(get_current_user),
):
    docs = service.get_docs_by_options("id", docs_id)
    return FindDocumentByOptionsResponse(
        message="",
        result=docs.result,
        meta=None
    )

@router.post("/", 
    response_model=CreateDocumentResponse,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude=None
)
@inject
def create_docs(
    background_tasks: BackgroundTasks,
    file: UploadFile      = File(...),
    document_name: str    = Form(...),
    request_id: UUID      = Form(...),
    service: DocsService = Depends(Provide[Container.docs_service]),
    current_user: User = Depends(get_current_user),
):
    metadata = CreateDocumentRequest(
        document_name=document_name,
        request_id=request_id
    )

    return service.upload_docs(
        file=file, 
        metadata=metadata, 
        background_tasks=background_tasks, 
        current_user=current_user
    )

@router.put("/{docs_id}",
    response_model=UpdateDocumentResponse,
    status_code=status.HTTP_200_OK,
    response_model_exclude=None
)
@inject
def update_docs(
    docs_id: UUID,
    background_tasks: BackgroundTasks,
    file: Optional[UploadFile]      = File(...),
    document_name: Optional[str]    = Form(...),
    service: DocsService = Depends(Provide[Container.docs_service]),
    current_user: User = Depends(get_current_user),
):
    metadata = UpdateDocumentRequest(document_name=document_name)
    docs = service.update_docs(
        docs_id=docs_id, 
        file=file, 
        metadata=metadata, 
        background_tasks=background_tasks,
        current_user=current_user
    )

    return UpdateDocumentResponse(
        message="Document updated successfully",
        result=docs.result,
        meta=None
    )

@router.delete("/{docs_id}",
    response_model=DeleteDocumentResponse,
    status_code=status.HTTP_200_OK,
    response_model_exclude=None               
)
@inject
def delete_docs(
    docs_id: UUID,
    service: DocsService = Depends(Provide[Container.docs_service]),
    current_user: User = Depends(get_current_user),
):
    service.delete_docs(docs_id)
    return DeleteDocumentResponse(
        message="Document deleted successfully",
        result=None,
        meta=None
    )

@router.get("/root/folders",
    status_code=status.HTTP_200_OK,
)
@inject
def list_root_folders_endpoint(
    service: DocsService = Depends(Provide[Container.docs_service]),
    current_user: User = Depends(get_current_user),
):
    return service.list_root_folder()
