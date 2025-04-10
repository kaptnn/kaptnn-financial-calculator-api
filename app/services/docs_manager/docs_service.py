from typing import Optional, TypedDict, Union
import uuid
from datetime import datetime
from fastapi import HTTPException
from app.core.exceptions import InternalServerError
from app.models.doc_model import Document
from app.services.base_service import BaseService
from app.repositories.docs_repo import DocsRepository

class DocumentDict(TypedDict):
    id: str
    company_name: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class DocsService(BaseService):
    def __init__(self, docs_repository: DocsRepository):
        self.docs_repository = docs_repository
        super().__init__(docs_repository)

    def get_all_docs(self, page: int, limit: int, sort: str, order: str):
        docs = self.docs_repository.get_all_docs()

        if not docs:
            return {"results": [], "total_items": 0, "total_pages": 0}

        if sort not in docs[0]:
            raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort}")

        reverse = (order.lower() == "desc")
        companies_sorted = sorted(docs, key=lambda x: x.get(sort, ""), reverse=reverse)

        total_items = len(companies_sorted)
        total_pages = (total_items + limit - 1) // limit
        offset = (page - 1) * limit
        paginated_companies = companies_sorted[offset : offset + limit]

        return {
            "results": paginated_companies,
            "total_items": total_items,
            "total_pages": total_pages,
        }

    def get_docs_by_options(self, option: str, value: Union[str, uuid.UUID]) -> DocumentDict:
        doc: Optional[Document] = self.docs_repository.get_docs_by_options(option, value) or (None, None)

        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")

        return DocumentDict(
            id=doc.id,

            created_at=doc.created_at,
            updated_at=doc.updated_at,
        )

    def upload_docs(self):
        uploaded_docs = self.docs_repository.create_docs()

    def update_docs(self):
        existing_docs = self.docs_repository.get_docs_by_options()

    def delete_docs(self):
        existing_docs = self.docs_repository.get_docs_by_options()
        
        if not existing_docs:
            raise HTTPException(status_code=404, detail="User not found")

        success = self.docs_repository.delete_docs(id)
        if not success:
            raise InternalServerError("Failed to delete company. Please try again later")

        return {"message": "Company deleted successfully"}