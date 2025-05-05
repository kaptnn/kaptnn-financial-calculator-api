import os
from typing import Any, Dict, Optional, Union
from uuid import UUID, uuid4
from fastapi import BackgroundTasks, HTTPException, UploadFile, status
from app.core.exceptions import InternalServerError
from app.schema.doc_schema import CreateDocumentRequest, CreateDocumentResponse, DeleteDocumentResponse, Document, FindAllDocumentsResponse, FindDocumentByOptionsResponse, UpdateDocumentRequest, UpdateDocumentResponse
from app.schema.user_schema import User
from app.services.base_service import BaseService
from app.repositories.docs_repo import DocsRepository
from fastapi_msal import MSALClientConfig, MSALAuthorization, UserInfo
from app.core.config import configs

class DocsService(BaseService):
    ALLOWED_SORTS = {"id", "company_name", "created_at"}
    ALLOWED_ORDERS = {"asc", "desc"}
    ALLOWED_FILTERS = {"id", "name", "year_of_assignment"}
    ALLOWED_MIME = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "image/jpeg",
        "image/jpg",
        "image/png"
    }
    MAX_SIZE = 10 * 1024 * 1024 

    def __init__(self, docs_repository: DocsRepository):
        self.docs_repository = docs_repository
        super().__init__(docs_repository)

    def get_all_docs(
        self, 
        page: int = 1, 
        limit: int = 100, 
        sort: str = "created_at", 
        order: str = "asc",
        filters: Optional[Dict[str, Any]] = None
    ) -> FindAllDocumentsResponse:
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
            
        return self.docs_repository.get_all_docs(
            page=page,
            limit=limit,
            sort=sort,
            order=order,
            filters=filters
        )

    def get_docs_by_options(
        self, 
        option: str, 
        value: Union[str, UUID]
    ) -> FindDocumentByOptionsResponse:
        if option not in self.ALLOWED_FILTERS:
            raise HTTPException(status_code=400, detail="Invalid option field")
        
        response = self.docs_repository.get_docs_by_options(option, value)

        if response.result is None:
            raise HTTPException(status_code=404, detail="Company not found")

        return response

    def upload_docs(
        self,
        file: UploadFile,
        metadata: CreateDocumentRequest,
        background_tasks: BackgroundTasks,
        current_user: User
    ) -> CreateDocumentResponse:
        if file.content_type not in self.ALLOWED_MIME:
            raise HTTPException(status_code=415, detail="Unsupported file type")

        file_id = uuid4()
        ext = os.path.splitext(file.filename)[1] or ""
        safe_name = f"{file_id}{ext}"

        upload_dir = "./utils"
        os.makedirs(upload_dir, exist_ok=True)

        tmp_path = os.path.join(upload_dir, safe_name)

        total = 0
        with open(tmp_path, "wb") as out:
            while True:
                chunk = file.file.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > self.MAX_SIZE:
                    out.close()
                    os.remove(tmp_path)
                    raise HTTPException(status_code=413, detail="File too large")
                out.write(chunk)

        background_tasks.add_task(
            self.docs_repository.push_to_onedrive,
            tmp_path, safe_name
        )

        record = self.docs_repository.create_docs(
            uploader=current_user.id,
            document_name=metadata.document_name,
            company=current_user.company_id,
            request_id=metadata.request_id,
            document_path=f"OneDrive:/YourAppFolder/{safe_name}",
            file_size=total,
            mime_type=file.content_type,
        )

        return CreateDocumentResponse(
            message="Upload processed",
            result=Document.model_validate(record),
            meta=None
        )

    def update_docs(
        self,
        docs_id: UUID,
        file: Optional[UploadFile],
        metadata: UpdateDocumentRequest,
        background_tasks: BackgroundTasks,
        current_user: User
    ) -> UpdateDocumentResponse:
        existing = self.docs_repository.get_docs_by_options("id", docs_id)
        if existing.result is None:
            raise HTTPException(status_code=404, detail="Document not found")

        update_data = metadata.model_dump(exclude_unset=True)

        if file:
            ext = os.path.splitext(file.filename)[1] or ""
            new_name = f"{docs_id}{ext}"
            tmp_path = f"/tmp/{new_name}"

            upload_dir = "./utils"
            tmp_path = os.path.join(upload_dir, new_name)

            total = 0
            with open(tmp_path, "wb") as out:
                while True:
                    chunk = file.file.read(1024 * 1024)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > self.MAX_SIZE:
                        out.close()
                        os.remove(tmp_path)
                        raise HTTPException(status_code=413, detail="File too large")
                    out.write(chunk)
            
            background_tasks.add_task(
                self.docs_repository.replace_onedrive_file,
                tmp_path, new_name
            )

            update_data["filename"] = new_name

        updated = self.docs_repository.update_docs(docs_id, UpdateDocumentRequest(**update_data))
        return UpdateDocumentResponse(
            message="Update document processed",
            result=updated.result,
            meta=None
        )

    def delete_docs(self, docs_id: UUID) -> DeleteDocumentResponse:
        existing_docs = self.docs_repository.get_docs_by_options("id", docs_id)
        if not existing_docs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

        response = self.docs_repository.delete_docs(docs_id)
        if not response:
            raise InternalServerError("Failed to delete document. Please try again later")
        
        return response
    
    def list_root_folder(self):
        return self.docs_repository.list_root_folder()