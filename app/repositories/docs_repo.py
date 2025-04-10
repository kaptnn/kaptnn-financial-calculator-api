import uuid
from sqlmodel import Session, select
from contextlib import AbstractContextManager
from typing import Callable, Literal, Optional, Union
from app.models.doc_model import Document
from app.repositories.base_repo import BaseRepository

class DocsRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Document)

    def get_all_docs(self) -> list[dict]:
        with self.session_factory() as session:
            statement = select(Document)
            result = session.exec(statement).all()
            
            return [
                {
                    "id": doc.id,
                    "request_id": doc.request_id,
                    "uploaded_by": doc.uploaded_by,
                    "company_id": doc.company_id,
                    "document_name": doc.document_name,
                    "document_path": doc.document_path,
                    "file_size": doc.file_size,
                    "mime_type": doc.mime_type,
                    "created_at": doc.created_at,
                    "updated_at": doc.updated_at,
                }
                for doc in result
            ]
        
    def get_docs_by_options(self, option: Literal["id", "request_id", "uploaded_by", "company_id"], value: Union[str, uuid.UUID]) -> Optional[Document]:
        if option in ["id", "request_id", "uploaded_by", "company_id"]:
            if isinstance(value, str):
                try:
                    value = uuid.UUID(value)
                except ValueError:
                    raise ValueError(f"Invalid UUID format for option {option}")

        with self.session_factory() as session:
            statement = select(Document).where(getattr(Document, option) == value)
            result = session.exec(statement).one_or_none()

            if result is None:
                return None

            session.expunge_all()
            return result
        
    def create_docs(
            self, 
            uploader: Union[str, uuid.UUID],
            document_name: str,
            company: Union[str, uuid.UUID],
            request_id: Optional[Union[str, uuid.UUID]] = None,
            document_path: Optional[str] = None,
            file_size: Optional[int] = None,
            mime_type: Optional[str] = None,
    ) -> Document:
        uploader_uuid = uuid.UUID(uploader) if isinstance(uploader, str) else uploader
        company_uuid = uuid.UUID(company) if isinstance(company, str) else company
        request_uuid = uuid.UUID(request_id) if request_id and isinstance(request_id, str) else request_id

        document = Document(
                id=None,
                request_id=request_uuid,
                uploaded_by=uploader_uuid,
                company_id=company_uuid,
                document_name=document_name,
                document_path=document_path,
                file_size=file_size,
                mime_type=mime_type,
                created_at=None,
                updated_at=None
            )

        with self.session_factory() as session:
            session.add(document)
            session.commit()
            session.refresh(document)

            session.expunge_all()
            return document
        
    def update_docs(self, id: Union[str, uuid.UUID], document: dict) -> Optional[Document]:
        doc_id = uuid.UUID(id) if isinstance(id, str) else id

        with self.session_factory() as session:
            statement = select(Document).where(Document.id == doc_id)
            result = session.exec(statement).one()

            if not result:
                return None
            
            for key, value in document.items():
                if hasattr(result, key):
                    setattr(result, key, value)

            session.add(result)
            session.commit()
            session.refresh(result)

            session.expunge_all()
            return result
        
    def delete_docs(self, id: Union[str, uuid.UUID]) -> bool:
        doc_id = uuid.UUID(id) if isinstance(id, str) else id

        with self.session_factory() as session:
            statement = select(Document).where(Document.id == doc_id)
            result = session.exec(statement).one()

            if not result:
                return False

            session.delete(result)
            session.commit()
            
            session.expunge_all()
            return True