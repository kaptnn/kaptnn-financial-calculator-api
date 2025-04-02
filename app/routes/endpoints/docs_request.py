from fastapi import APIRouter
from app.core.middleware import inject

router = APIRouter(prefix="/docs-request", tags=["docs requests"])

@router.get("/")
@inject
def get_all_docs_requests():
    pass

@router.get("/id/{id}")
@inject
def get_docs_request_by_id():
    pass

@router.post("/")
@inject
def create_docs_request():
    pass

@router.put("/id/{id}")
@inject
def update_docs_request():
    pass

@router.delete("/id/{id}")
@inject
def delete_docs_request():
    pass