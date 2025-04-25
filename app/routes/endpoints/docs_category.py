import uuid
from fastapi import APIRouter, Depends, Query, status
from dependency_injector.wiring import Provide
from app.core.container import Container
from app.core.middleware import inject
from app.core.dependencies import get_current_user
from app.services.user_service import UserDict
from app.schema.doc_category_schema import FindDocumentCategoryByOptionsResponse, CreateDocumentCategoryRequest, CreateDocumentCategoryResponse, UpdateDocumentCategoryRequest, UpdateDocumentCategoryResponse, DeleteDocumentCategoryResponse
from app.services.docs_manager.docs_category_service import DocsCategoryService

router = APIRouter(prefix="/docs-category", tags=["docs categories"])

@router.get("/", response_model=dict, status_code=status.HTTP_200_OK)
@inject
def get_all_docs_categories(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(5, ge=1, le=100, description="Number of users per page"),
    sort: str = Query("created_at", description="Field to sort by"),
    order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order (asc or desc)"),
    service: DocsCategoryService = Depends(Provide[Container.docs_category_service]),
    current_user: UserDict = Depends(get_current_user),
):
    docs_categories = service.get_all_docs_categories(page=page, limit=limit, sort=sort, order=order)
    return {
        "message": "Docs categories retrieved successfully",
        "result": docs_categories["result"],
        "pagination": {
            "current_page": page,
            "total_pages": docs_categories["total_pages"],
            "total_items": docs_categories["total_items"],
        },
    }

@router.get("/{docs_category_id}", response_model=FindDocumentCategoryByOptionsResponse, status_code=status.HTTP_200_OK)
@inject
def get_docs_category_by_id(
    docs_category_id: uuid.UUID,
    service: DocsCategoryService = Depends(Provide[Container.docs_category_service]),
    current_user: UserDict = Depends(get_current_user),
):
    result = service.get_docs_category_by_options(option="id", value=docs_category_id)
    return {
        "message": "Company retrieved successfully",
        "result": result,
    }

@router.post("/", response_model=CreateDocumentCategoryResponse, status_code=status.HTTP_201_CREATED)
@inject
def create_docs_category(
    docs_category: CreateDocumentCategoryRequest,
    service: DocsCategoryService = Depends(Provide[Container.docs_category_service]),
    current_user: UserDict = Depends(get_current_user),
):
    return service.create_docs_category(docs_category)

@router.put("/{docs_category_id}", response_model=UpdateDocumentCategoryResponse, status_code=status.HTTP_200_OK)
@inject
def update_docs_category(
    docs_category_id: uuid.UUID,
    docs_category: UpdateDocumentCategoryRequest,
    service: DocsCategoryService = Depends(Provide[Container.docs_category_service]),
    current_user: UserDict = Depends(get_current_user),
):
    result = service.update_docs_category(docs_category)
    return {
        "message": "Company updated successfully",
        "result": result,
    }

@router.delete("/{docs_category_id}", response_model=DeleteDocumentCategoryResponse, status_code=status.HTTP_200_OK)
@inject
def delete_docs_category(
    docs_category_id: uuid.UUID,
    service: DocsCategoryService = Depends(Provide[Container.docs_category_service]),
    current_user: UserDict = Depends(get_current_user),
):
    return service.delete_docs_category(docs_category_id)