import uuid
from datetime import datetime
from typing import Tuple, TypedDict, Optional, Union
from fastapi import HTTPException
from app.core.exceptions import InternalServerError
from app.repositories.docs_category_repo import DocsCategoryRepository 
from app.services.base_service import BaseService
from app.schema.doc_category_schema import CreateDocumentCategoryRequest, CreateDocumentCategoryResponse, DeleteDocumentCategoryResponse, DocumentCategory, UpdateDocumentCategoryRequest, UpdateDocumentCategoryResponse

class DocsCategoryDict(TypedDict):
    id: str
    name: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class DocsCategoryService(BaseService):
    def __init__(self, docs_category_repository: DocsCategoryRepository):
        self.docs_category_repository = docs_category_repository
        super().__init__(docs_category_repository)

    def get_all_docs_categories(self, page: int, limit: int, sort: str, order: str) -> dict:
        docs_categories = self.docs_category_repository.get_all_docs_category()

        if not docs_categories:
            return {"result": [], "total_items": 0, "total_pages": 0}

        if sort not in docs_categories[0]:
            raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort}")

        reverse = (order.lower() == "desc")
        companies_sorted = sorted(docs_categories, key=lambda x: x.get(sort, ""), reverse=reverse)

        total_items = len(companies_sorted)
        total_pages = (total_items + limit - 1) // limit
        offset = (page - 1) * limit
        paginated_docs_categories = companies_sorted[offset : offset + limit]

        return {
            "result": paginated_docs_categories,
            "total_items": total_items,
            "total_pages": total_pages,
        }

    def get_docs_category_by_options(self, option: str, value: Union[str, uuid.UUID]) -> Optional[Tuple[DocsCategoryDict]]:
        result = self.docs_category_repository.get_docs_category_by_options(option, value)

        if not result:
            raise HTTPException(status_code=404, detail="Document category not found")
        
        return DocsCategoryDict(
            id=str(result.id),
            name=result.name,
            created_at=result.created_at,
            updated_at=result.updated_at,
        )

    def create_docs_category(self, docs_category: CreateDocumentCategoryRequest) -> CreateDocumentCategoryResponse:
        new_docs_category = self.docs_category_repository.create_docs_category(name=docs_category.name)

        if not new_docs_category:
            raise InternalServerError("Failed to create document category. Please try again later")

        result = DocumentCategory(
            id=str(new_docs_category.id),
            name=new_docs_category.name,
            created_at=new_docs_category.created_at,
            updated_at=new_docs_category.updated_at,
        )

        return CreateDocumentCategoryResponse(
            message="Document Category successfully registered", 
            result=result.model_dump()
        )

    def update_docs_category(self, docs_category_id: str, docs_category: UpdateDocumentCategoryRequest) -> UpdateDocumentCategoryResponse:
        existing_docs_category = self.docs_category_repository.get_docs_category_by_options("id", docs_category_id)
        
        if not existing_docs_category:
            raise HTTPException(status_code=404, detail="Document Category not found")

        updated_docs_category = self.docs_category_repository.update_docs_category(docs_category_id, docs_category)

        return DocumentCategory(
            id=updated_docs_category.id,
            name=updated_docs_category.name,
            created_at=updated_docs_category.created_at,
            updated_at=updated_docs_category.updated_at,
        )

    def delete_docs_category(self, docs_category_id: str) -> DeleteDocumentCategoryResponse:
        existing_docs_category = self.docs_category_repository.get_docs_category_by_options("id", docs_category_id)
        if not existing_docs_category:
            raise HTTPException(status_code=404, detail="Document category not found")

        success = self.docs_category_repository.delete_docs_category(docs_category_id)
        if not success:
            raise InternalServerError("Failed to delete document category. Please try again later")
        
        return {"message": "Document category deleted successfully"}
