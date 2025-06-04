from datetime import datetime
from uuid import UUID
from sqlmodel import Session, func, select
from contextlib import AbstractContextManager
from typing import Any, Callable, Dict, Union, Optional
from app.models.doc_request_model import DocumentRequest
from app.repositories.base_repo import BaseRepository
from app.schema.doc_request_schema import FindAllDocumentReqsResponse, FindDocumentReqByOptionsResponse, UpdateDocumentReqRequest, UpdateDocumentReqResponse, DeleteDocumentReqResponse, DocumentReq as DocumentRequestSchema

class DocsRequestRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, DocumentRequest)

    def get_all_docs_requests(
        self,
        page: int = 1,
        limit: int = 100,
        sort: str = "created_at",
        order: str = "asc",
        filters: Optional[Dict[str, Any]] = None
    ) -> FindAllDocumentReqsResponse:
        with self.session_factory() as session:
            statement = select(DocumentRequest)

            if filters:
                if status := filters.get("status"):
                    statement = statement.where(DocumentRequest.status == status)
                if category_id := filters.get("category_id"):
                    statement = statement.where(DocumentRequest.category_id == category_id)
                if target_user_id := filters.get("target_user_id"):
                    statement = statement.where(DocumentRequest.target_user_id == target_user_id)
                if admin_id := filters.get("admin_id"):
                    statement = statement.where(DocumentRequest.admin_id == admin_id)
                if name_query := filters.get("name"):
                    statement = statement.where(DocumentRequest.request_title.ilike(f"%{name_query}%"))

            sort_column = getattr(DocumentRequest, sort)
            if order.lower() == "desc":
                sort_column = sort_column.desc()
            statement = statement.order_by(sort_column)

            total_items = session.exec(select(func.count()).select_from(statement.subquery())).one()
            total_pages = (total_items + limit - 1) // limit
            offset = (page - 1) * limit

            statement = statement.offset(offset).limit(limit)
            result = session.exec(statement).all()

            docs_requests_list = [DocumentRequestSchema.model_validate(docs) for docs in result]

            return FindAllDocumentReqsResponse(
                message="Success retrieved data from repository",
                result=docs_requests_list,
                meta={ 'current_page': page, "total_items": total_items, 'total_pages': total_pages }
            )
        
    def get_docs_request_by_options(
        self, 
        option: str, 
        value: Union[str, UUID]
    ) -> FindDocumentReqByOptionsResponse:
        with self.session_factory() as session:
            statement = select(DocumentRequest).where(getattr(DocumentRequest, option) == value)
            result = session.exec(statement).all()

            if option in ("id"):
                if not result:
                    return FindDocumentReqByOptionsResponse(
                        message="No document request found",
                        result=None,
                        meta=None,
                    )

                docs_request_obj = result[0]
                docs_request_schema = DocumentRequestSchema.model_validate(docs_request_obj)
                return FindDocumentReqByOptionsResponse(
                    message="Success retrieved data from repository",
                    result=docs_request_schema,
                    meta=None
                )
        
    def create_docs_request(
        self,
        request_title: str,
        request_desc: str,
        admin: UUID,
        target_user: UUID,
        category: UUID,
        due_date: datetime,
    ) -> DocumentRequest:
        with self.session_factory() as session:
            document_request = DocumentRequest(
                admin_id=admin,
                request_title=request_title,
                request_desc=request_desc,
                target_user_id=target_user,
                category_id=category,
                due_date=due_date,
            )

            session.add(document_request)
            session.commit()
            session.refresh(document_request)

            session.expunge_all()
            return document_request
        
    def update_docs_request(
        self, 
        doc_request_id: UUID, 
        document_request_info: UpdateDocumentReqRequest
    ) -> UpdateDocumentReqResponse:
        with self.session_factory() as session:
            statement = select(DocumentRequest).where(DocumentRequest.id == doc_request_id)
            result = session.exec(statement).one()

            data = document_request_info.model_dump(exclude_unset=True)
            for field, value, in data.items():
                setattr(result, field, value)

            session.add(result)
            session.commit()
            session.refresh(result)

            response = DocumentRequestSchema.model_validate(result)

            return UpdateDocumentReqResponse(
                message="Success updated data from repository",
                result=response,
                meta=None
            )

    def delete_docs_request(self, doc_request_id: UUID) -> DeleteDocumentReqResponse:
        with self.session_factory() as session:
            docs_request = session.get(DocumentRequest, doc_request_id)
            
            if not docs_request:
                return DeleteDocumentReqResponse(
                    message="Document request not found",
                    result=None,
                    meta=None
                )

            session.delete(docs_request)
            session.commit()

            return DeleteDocumentReqResponse(
                message="Success deleted data from repository",
                result=None,
                meta=None
            )