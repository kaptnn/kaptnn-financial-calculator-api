from uuid import UUID
from typing import Any, Dict, Optional, Union
from fastapi import HTTPException, status
from app.core.exceptions import InternalServerError
from app.repositories.docs_category_repo import DocsCategoryRepository 
from app.services.base_service import BaseService
from app.schema.doc_category_schema import CreateDocumentCategoryRequest, CreateDocumentCategoryResponse, DeleteDocumentCategoryResponse, DocumentCategory, UpdateDocumentCategoryRequest, UpdateDocumentCategoryResponse, FindAllDocumentCategoriesResponse, FindDocumentCategoryByOptionsResponse

class DocsCategoryService(BaseService):
    ALLOWED_SORTS = {"id", "created_at"}
    ALLOWED_ORDERS = {"asc", "desc"}
    ALLOWED_FILTERS = {"id", "name"}

    def __init__(self, docs_category_repository: DocsCategoryRepository):
        self.docs_category_repository = docs_category_repository
        super().__init__(docs_category_repository)

    def get_all_docs_categories(
        self, 
        page: int = 1, 
        limit: int = 100, 
        sort: str = "created_at", 
        order: str = "asc",
        filters: Optional[Dict[str, Any]] = None
    ) -> FindAllDocumentCategoriesResponse:
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
        
        return self.docs_category_repository.get_all_docs_category(
            page=page,
            limit=limit,
            sort=sort,
            order=order,
            filters=filters
        )
        

    def get_docs_category_by_options(
        self, 
        option: str, 
        value: Union[str, UUID]
    ) -> FindDocumentCategoryByOptionsResponse:
        if option not in self.ALLOWED_FILTERS:
            raise HTTPException(status_code=400, detail="Invalid option field")
        
        response = self.docs_category_repository.get_docs_category_by_options(option, value)

        if response.result is None:
            raise HTTPException(status_code=404, detail="Document category not found")
        
        return response

    def create_docs_category(self, docs_category: CreateDocumentCategoryRequest) -> CreateDocumentCategoryResponse:
        existing = self.docs_category_repository.get_docs_category_by_options("name", docs_category.name)
        if existing.result is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A company with this name is already registered."
            )
        
        new_docs_category = self.docs_category_repository.create_docs_category(
            name=docs_category.name
        )

        if not new_docs_category:
            raise InternalServerError("Failed to create document category. Please try again later")

        return CreateDocumentCategoryResponse(
            message="Document category successfully registered",
            result=None,
            meta=None
        )

    def update_docs_category(self, docs_category_id: UUID, docs_category: UpdateDocumentCategoryRequest) -> UpdateDocumentCategoryResponse:
        existing_docs_category = self.docs_category_repository.get_docs_category_by_options("id", docs_category_id)
        
        if existing_docs_category.result is None:
            raise HTTPException(status_code=404, detail="Document Category not found")

        response = self.docs_category_repository.update_docs_category(docs_category_id, docs_category)

        if not response:
            raise InternalServerError("Failed to update user. Please try again later")

        return response

    def delete_docs_category(self, docs_category_id: UUID) -> DeleteDocumentCategoryResponse:
        existing_docs_category = self.docs_category_repository.get_docs_category_by_options("id", docs_category_id)
        if not existing_docs_category:
            raise HTTPException(status_code=404, detail="Document category not found")

        response = self.docs_category_repository.delete_docs_category(docs_category_id)
        if not response:
            raise InternalServerError("Failed to delete document category. Please try again later")
        
        return response
