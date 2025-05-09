import os
from uuid import UUID
import requests
from sqlmodel import Session, func, select
from contextlib import AbstractContextManager
from typing import Any, Callable, Dict, Optional, Union
from app.models.doc_model import Document
from app.repositories.base_repo import BaseRepository
from app.schema.doc_schema import DeleteDocumentResponse, FindAllDocumentsResponse, Document as DocumentSchema, FindDocumentByOptionsResponse, UpdateDocumentRequest, UpdateDocumentResponse
from app.core.msal import get_app_response, MS_GRAPH_BASE_URL, client

class DocsRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Document)

    def get_all_docs(
        self,
        page: int = 1,
        limit: int = 100,
        sort: str = "created_at",
        order: str = "asc",
        filters: Optional[Dict[str, Any]] = None
    ) -> FindAllDocumentsResponse:
        with self.session_factory() as session:
            statement = select(Document)

            if filters:
                if year_of_assignment := filters.get("year_of_assignment"):
                    statement = statement.where(Document.year_of_assignment == year_of_assignment)
                if name_query := filters.get("name"):
                    statement = statement.where(Document.company_name.ilike(f"%{name_query}%"))

            sort_column = getattr(Document, sort)
            if order.lower() == "desc":
                sort_column = sort_column.desc()
            statement = statement.order_by(sort_column)

            total_items = session.exec(select(func.count()).select_from(statement.subquery())).one()
            total_pages = (total_items + limit - 1) // limit
            offset = (page - 1) * limit

            statement = statement.offset(offset).limit(limit)
            result = session.exec(statement).all()
            
            documents_list = [DocumentSchema.model_validate(d) for d in result]
            
            return FindAllDocumentsResponse(
                message="Success retrieved data from repository",
                result=documents_list,
                meta={ 'current_page': page, "total_items": total_items, 'total_pages': total_pages }
            )
        
    def get_docs_by_options(self, option: str, value: Union[str, UUID]) -> FindDocumentByOptionsResponse:
        with self.session_factory() as session:
            statement = select(Document).where(getattr(Document, option) == value)
            result = session.exec(statement).all()

            if option in ("id"):
                if not result:
                    return FindDocumentByOptionsResponse(
                        message="Document not found",
                        result=None,
                        meta=None,
                    )

                docs_obj = result[0]
                docs_schema = DocumentSchema.model_validate(docs_obj)
                return FindDocumentByOptionsResponse(
                    message="Success retrieved data from repository",
                    result=docs_schema,
                    meta=None
                )
        
    def create_docs(
        self, 
        uploader: UUID,
        document_name: str,
        company: UUID,
        request_id: UUID = None,
        document_path: Optional[str] = None,
        file_size: Optional[int] = None,
        mime_type: Optional[str] = None,
    ) -> Document:
        with self.session_factory() as session:
            document = Document(
                request_id=request_id,
                uploaded_by=uploader,
                company_id=company,
                document_name=document_name,
                document_path=document_path,
                file_size=file_size,
                mime_type=mime_type,
            )

            session.add(document)
            session.commit()
            session.refresh(document)

            session.expunge_all()
            return document
        
    def update_docs(self, docs_id: UUID, document_info: UpdateDocumentRequest) -> UpdateDocumentResponse:
        with self.session_factory() as session:
            statement = select(Document).where(Document.id == docs_id)
            docs = session.exec(statement).one()

            data = document_info.model_dump(exclude_unset=True)
            for field, value, in data.items():
                setattr(docs, field, value)

            session.add(docs)
            session.commit()
            session.refresh(docs)

            DocumentSchema.model_validate(docs)

            return UpdateDocumentResponse(
                message="Success updated data from repository",
                result=None,
                meta=None
            )
        
    def delete_docs(self, docs_id: UUID) -> DeleteDocumentResponse:
        with self.session_factory() as session:
            docs = session.get(Document, docs_id)

            if not docs:
                return DeleteDocumentResponse(
                    message="Document not found",
                    result=None,
                    meta=None
                )

            session.delete(docs)
            session.commit()
            
            return DeleteDocumentResponse(
                message="Success deleted data from repository",
                result=None,
                meta=None
            )

    def push_to_onedrive(
        self, 
        tmp_path: str,
        remote_name: str
    ) -> None:
        response = get_app_response()
        token = response["access_token"]

        session_url = (
            MS_GRAPH_BASE_URL+"/drive/root:/Documents/{name}:/createUploadSession"
        ).format(name=remote_name)

        resp = requests.post(
            session_url,
            headers={"Authorization": f"Bearer {token}"},
            json={"item": {"@microsoft.graph.conflictBehavior": "replace"}}
        )
        resp.raise_for_status()
        upload_url = resp.json()["uploadUrl"]

        file_size = os.path.getsize(tmp_path)
        chunk_size = 10 * 1024 * 1024
        with open(tmp_path, "rb") as f:
            start = 0
            while start < file_size:
                chunk = f.read(chunk_size)
                end = start + len(chunk) - 1
                headers = {
                    "Content-Range": f"bytes {start}-{end}/{file_size}"
                }
                put = requests.put(upload_url, headers=headers, data=chunk)
                put.raise_for_status()
                start = end + 1

        os.remove(tmp_path)

    def replace_onedrive_file(
        self, 
        tmp_path: str, 
        remote_name: str
    ) -> None:
        self.push_to_onedrive(tmp_path, remote_name)
    
    def current_user_drive(self):
        url = f"{MS_GRAPH_BASE_URL}/me/drive"

    def current_user_all_drives(self):
        url = f"{MS_GRAPH_BASE_URL}/me/drives"

    def list_root_folder_by_current_user(self):
        msal = get_app_response()
        token = msal["access_token"]

        url = f"{MS_GRAPH_BASE_URL}/drives/b!WZrvKxB3Tkizoko0leI02brJ6Cnv1jxIgW3kc9-ojUU-iNsh-Uj5SbaKpP8AHzMd/root/children"
        print(url)
        response = requests.get(url, headers={"Authorization": f"Bearer {token}"})

        print(response.json())

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to list root folder:  {response.status_code}")

    def list_root_folder_by_current_user_path_root(self):
        url = f"{MS_GRAPH_BASE_URL}/me/drive/root:/path/to/folder:/children"

    def list_root_folder_by_current_user_path_root_and_id(self, item_id: str):
        url = f"{MS_GRAPH_BASE_URL}/me/drive/items/{item_id}:/path/to/folder:/children"

    def get_drive_item_by_current_user(self, item_id: str):
        url = f"{MS_GRAPH_BASE_URL}/me/drive/items/{item_id}"

    def get_drive_special_folder_by_current_user(self, special_id: str):
        url = f"{MS_GRAPH_BASE_URL}/me/drive/special/{special_id}"

    def get_item_by_current_user_path_root(self):
        url = f"{MS_GRAPH_BASE_URL}/me/drive/root:/path/to/file"

    def get_item_by_current_user_path_path_root_and_id(self, item_id: str):
        url = f"{MS_GRAPH_BASE_URL}/me/drive/items/{item_id}:/path/to/file"

    def get_drive_by_id(self, drive_id: str):
        url = f"{MS_GRAPH_BASE_URL}/drives/{drive_id}"

    def list_root_folder_by_drive_id(self, drive_id: str):
        url = f"{MS_GRAPH_BASE_URL}/drives/{drive_id}/root/children"

    def get_shared_item(self, share_id: str):
        url = f"{MS_GRAPH_BASE_URL}/shares/{share_id}"

    def get_site_drive(self, site_id: str):
        url = f"{MS_GRAPH_BASE_URL}/sites/{site_id}/drive"

    def get_all_site_drive(self, site_id: str):
        url = f"{MS_GRAPH_BASE_URL}/sites/{site_id}/drives"