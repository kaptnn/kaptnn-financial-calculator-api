from typing import Any, Dict, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from dependency_injector.wiring import Provide
from app.core.container import Container
from app.core.middleware import inject
from app.core.dependencies import get_current_user
from app.schema.doc_category_schema import FindDocumentCategoryByOptionsResponse, CreateDocumentCategoryRequest, CreateDocumentCategoryResponse, UpdateDocumentCategoryRequest, UpdateDocumentCategoryResponse, DeleteDocumentCategoryResponse, FindAllDocumentCategoriesResponse
from app.services.docs_manager.docs_category_service import DocsCategoryService

router = APIRouter(prefix="/document-categories", tags=["Document Category"])

@router.get("/", 
    response_model=FindAllDocumentCategoriesResponse, 
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True)
@inject
def get_all_docs_categories(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of users per page"),
    sort: str = Query("created_at", description="Field to sort by"),
    order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order (asc or desc)"),
    name: Optional[str] = Query(None, description="Filter by name substring"),
    service: DocsCategoryService = Depends(Provide[Container.docs_category_service]),
    current_user = Depends(get_current_user),
):
    filters: Dict[str, Any] = {}
    if name:
        filters["name"] = name

    docs_categories = service.get_all_docs_categories(
        page=page, 
        limit=limit, 
        sort=sort, 
        order=order,
        filters=filters
    )

    return {
        "message": "Document categories retrieved successfully",
        "result": docs_categories.result,
        "meta": {
            "current_page": page,
            "total_pages": docs_categories.meta.total_pages,
            "total_items": docs_categories.meta.total_items,
        },
    }

@router.get("/summary/category", 
    status_code=status.HTTP_200_OK,  
    response_model_exclude_none=True)
@inject
def get_doc_category_count(
    service: DocsCategoryService = Depends(Provide[Container.docs_category_service]),
    current_user = Depends(get_current_user),
):
    summary = service.get_category_count()
    return {
        "message": "Docs category summary retrieved successfully",
        "result": summary,
        "meta": None,
    }

@router.get("/{docs_category_id}", 
    response_model=FindDocumentCategoryByOptionsResponse, 
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True)
@inject
def get_docs_category_by_id(
    docs_category_id: UUID,
    service: DocsCategoryService = Depends(Provide[Container.docs_category_service]),
    current_user = Depends(get_current_user),
):
    docs = service.get_docs_category_by_options("id", docs_category_id)
    return FindDocumentCategoryByOptionsResponse(
        message="Document category retrieved successfully",
        result=docs.result,
        meta=None
    )

@router.post("/", 
    response_model=CreateDocumentCategoryResponse, 
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True)
@inject
def create_docs_category(
    docs_category: CreateDocumentCategoryRequest,
    service: DocsCategoryService = Depends(Provide[Container.docs_category_service]),
    current_user = Depends(get_current_user),
):
    return service.create_docs_category(docs_category)

@router.put("/{docs_category_id}", 
    response_model=UpdateDocumentCategoryResponse, 
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True)
@inject
def update_docs_category(
    docs_category_id: UUID,
    docs_category_info: UpdateDocumentCategoryRequest,
    service: DocsCategoryService = Depends(Provide[Container.docs_category_service]),
    current_user = Depends(get_current_user),
):
    docs = service.update_docs_category(docs_category_id, docs_category_info)
    return UpdateDocumentCategoryResponse(
        message="Document category updated successfully",
        result=docs.result,
        meta=None
    )

@router.delete("/{docs_category_id}", 
    response_model=DeleteDocumentCategoryResponse, 
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True)
@inject
def delete_docs_category(
    docs_category_id: UUID,
    service: DocsCategoryService = Depends(Provide[Container.docs_category_service]),
    current_user = Depends(get_current_user),
):
    service.delete_docs_category(docs_category_id)
    return DeleteDocumentCategoryResponse(
        message="Document category deleted successfully",
        result=None,
        meta=None
    )