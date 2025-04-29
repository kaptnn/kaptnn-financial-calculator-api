from uuid import UUID
from sqlmodel import Session, func, select
from contextlib import AbstractContextManager
from typing import Any, Callable, Dict, Union, Optional
from app.models.doc_category_model import DocumentCategory
from app.repositories.base_repo import BaseRepository
from app.schema.doc_category_schema import FindAllDocumentCategoriesResponse, FindDocumentCategoryByOptionsResponse, DocumentCategory as DocumentCategorySchema, UpdateDocumentCategoryRequest, UpdateDocumentCategoryResponse, DeleteDocumentCategoryResponse

class DocsCategoryRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, DocumentCategory)
        
    def get_all_docs_category(
        self, 
        page: int = 1,
        limit: int = 100,
        sort: str = "created_at",
        order: str = "asc",
        filters: Optional[Dict[str, Any]] = None
    ) -> FindAllDocumentCategoriesResponse:
        with self.session_factory() as session:
            statement = select(DocumentCategory)

            if filters:
                if name_query := filters.get("name"):
                    statement = statement.where(DocumentCategory.name.ilike(f"%{name_query}%"))
            
            sort_column = getattr(DocumentCategory, sort)
            if order.lower() == "desc":
                sort_column = sort_column.desc()
            statement = statement.order_by(sort_column)

            total_items = session.exec(select(func.count()).select_from(statement.subquery())).one()
            total_pages = (total_items + limit - 1) // limit
            offset = (page - 1) * limit

            statement = statement.offset(offset).limit(limit)
            result = session.exec(statement).all()

            docs_categories_list = [DocumentCategorySchema.model_validate(docs) for docs in result]

            return FindAllDocumentCategoriesResponse(
                message="Success retrieved data from repository",
                result=docs_categories_list,
                meta={ 'current_page': page, "total_items": total_items, 'total_pages': total_pages }
            )
        
    def get_docs_category_by_options(self, option: str, value: Union[str, UUID]) -> FindDocumentCategoryByOptionsResponse:
        with self.session_factory() as session:
            statement = select(DocumentCategory).where(getattr(DocumentCategory, option) == value)
            result = session.exec(statement).one_or_none()

            if option in ("id", "name"):
                if not result:
                    return FindAllDocumentCategoriesResponse(
                        message="No document category found",
                        result=None,
                        meta=None,
                    )

                docs_category_obj = result[0]
                docs_category_schema = DocumentCategorySchema.model_validate(docs_category_obj)
                return FindAllDocumentCategoriesResponse(
                    message="Success retrieved data from repository",
                    result=docs_category_schema,
                    meta=None
                )
        
    def create_docs_category(self, name: str) -> DocumentCategory:
        with self.session_factory() as session:
            docs_category = DocumentCategory(name=name)

            session.add(docs_category)
            session.commit()
            session.refresh(docs_category)

            session.expunge_all()
            return docs_category
        
    def update_docs_category(self, docs_id: UUID, docs_category_info: UpdateDocumentCategoryRequest) -> UpdateDocumentCategoryResponse:
        with self.session_factory() as session:
            statement = select(DocumentCategory).where(DocumentCategory.id == docs_id)
            result = session.exec(statement).one()

            data = docs_category_info.model_dump(exclude_unset=True)
            for field, value, in data.items():
                setattr(result, field, value)

            session.merge(result)
            session.commit()
            session.refresh(result)

            DocumentCategorySchema.model_validate(result)

            return UpdateDocumentCategoryResponse(
                message="Success updated data from repository",
                result=None,
                meta=None,
            )
        
    def delete_docs_category(self, docs_id: UUID) -> DeleteDocumentCategoryResponse:
        with self.session_factory() as session:
            result = session.get(DocumentCategory, docs_id)

            if not result:
                return DeleteDocumentCategoryResponse(
                    message="Document category not found",
                    result=None,
                    meta=None
                )

            session.delete(result)
            session.commit()
            
            return DeleteDocumentCategoryResponse(
                message="Success deleted data from repository",
                result=None,
                meta=None
            )