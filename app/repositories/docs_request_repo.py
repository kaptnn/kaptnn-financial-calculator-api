import uuid
from sqlmodel import Session, select
from contextlib import AbstractContextManager
from typing import Callable, List, Literal, Union, Optional
from app.models.doc_request_model import DocumentRequest
from app.repositories.base_repo import BaseRepository

class DocsRequestRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, DocumentRequest)

    def get_all_docs_requests(self) -> List[DocumentRequest]:
        with self.session_factory() as session:
            statement = select(DocumentRequest)
            result = session.exec(statement).all()
            
            data = [
                {
                    "id": docs_request.id,
                    "admin_id": docs_request.admin_id,
                    "request_title": docs_request.request_title,
                    "request_desc": docs_request.request_desc,
                    "target_user_id": docs_request.target_user_id,
                    "category_id": docs_request.category_id,
                    "due_date": docs_request.due_date,
                    "upload_date": docs_request.upload_date,
                    "status": docs_request.status,
                    "updated_at": docs_request.updated_at,
                    "created_at": docs_request.created_at,
                }
                for docs_request in result
            ]

            return data
        
    def get_docs_request_by_options(
        self, 
        option: Literal["id", "admin_id", "target_user_id", "category_id"], 
        value: Union[str, uuid.UUID]
    ) -> Optional[DocumentRequest]:
        if option in ["id", "admin_id", "target_user_id", "category_id"]:
            if isinstance(value, str):
                try:
                    value = uuid.UUID(value)
                except ValueError:
                    raise ValueError(f"Invalid UUID format for option {option}")

        with self.session_factory() as session:
            statement = select(DocumentRequest).where(getattr(DocumentRequest, option) == value)
            result = session.exec(statement).one_or_none()

            if result is None:
                return None

            session.expunge_all()
            return result
        
    def create_docs_request(
        self,
        admin,
        request_title,
        request_desc,
        target_user,
        category,
        due_date,
    ) -> DocumentRequest:
        admin_uuid = uuid.UUID(admin) if isinstance(admin, str) else admin
        target_user_uuid = uuid.UUID(target_user) if isinstance(target_user, str) else target_user
        category_uuid = uuid.UUID(category) if category and isinstance(category, str) else category

        document_request = DocumentRequest(
                admin_id=admin_uuid,
                request_title=request_title,
                request_desc=request_desc,
                target_user_id=target_user_uuid,
                category_id=category_uuid,
                due_date=due_date,
            )

        with self.session_factory() as session:
            session.add(document_request)
            session.commit()
            session.refresh(document_request)

            session.expunge_all()
            return document_request
        
    def update_docs_request(self, id: Union[str, uuid.UUID], document_request: DocumentRequest) -> Optional[DocumentRequest]:
        doc_request_id = uuid.UUID(id) if isinstance(id, str) else id

        with self.session_factory() as session:
            statement = select(DocumentRequest).where(DocumentRequest.id == doc_request_id)
            result = session.exec(statement).one()

            if not result:
                return None

            for key, value in document_request.items():
                if hasattr(result, key):
                    setattr(result, key, value)

            session.add(result)
            session.commit()
            session.refresh(result)

            session.expunge_all()
            return result

    def delete_docs_request(self, id: Union[str, uuid.UUID]) -> bool:
        doc_request_id = uuid.UUID(id) if isinstance(id, str) else id

        with self.session_factory() as session:
            statement = select(DocumentRequest).where(DocumentRequest.id == doc_request_id)
            result = session.exec(statement).one()

            if not result:
                return False

            session.delete(result)
            session.commit()
            
            session.expunge_all()
            return True