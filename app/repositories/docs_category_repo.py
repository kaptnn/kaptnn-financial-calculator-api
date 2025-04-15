import uuid
from sqlmodel import Session, select
from contextlib import AbstractContextManager
from typing import Callable, List, Union, Optional, Tuple
from app.models.doc_category_model import DocumentCategory
from app.repositories.base_repo import BaseRepository

class DocsCategoryRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, DocumentCategory)
        
    def get_all_docs_category(self) -> List[DocumentCategory]:
        with self.session_factory() as session:
            statement = select(DocumentCategory)
            result = session.exec(statement).all()
            
            data = [
                {
                    "id": docs_category.id,
                    "name": docs_category.name,
                    "created_at": docs_category.created_at,
                    "updated_at": docs_category.updated_at,
                }
                for docs_category in result
            ]

            return data
        
    def get_docs_category_by_options(self, option: str, value: Union[str, uuid.UUID]) -> Optional[Tuple[DocumentCategory]]:
        if option not in ["id"]:
            raise ValueError("Invalid option")

        with self.session_factory() as session:
            statement = select(DocumentCategory).where(getattr(DocumentCategory, option) == value)
            result = session.exec(statement).one_or_none()

            if result is None:
                return None
            
            session.expunge_all()
            return result
        
    def create_docs_category(self, name: str) -> DocumentCategory:
        with self.session_factory() as session:
            docs_category = DocumentCategory(name=name, id=None, created_at=None, updated_at=None)

            session.add(docs_category)
            session.commit()
            session.refresh(docs_category)

            session.expunge_all()
            return docs_category
        
    def update_docs_category(self, id: str, docs_category: DocumentCategory) -> Optional[DocumentCategory]:
        with self.session_factory() as session:
            statement = select(DocumentCategory).where(DocumentCategory.id == id)
            result = session.exec(statement).one()

            if not result:
                return None
            
            result = result.model_copy(update=docs_category.model_dump(exclude_unset=True))
            
            session.merge(result)
            session.commit()
            session.refresh(result)

            session.expunge_all()
            return result
        
    def delete_docs_category(self, id: str) -> bool:
        with self.session_factory() as session:
            statement = select(DocumentCategory).where(DocumentCategory.id == id)
            result = session.exec(statement).one()

            if not result:
                return False

            session.delete(result)
            session.commit()
            
            session.expunge_all()
            return True