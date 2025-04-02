from fastapi import APIRouter
from app.core.middleware import inject

router = APIRouter(prefix="/docs", tags=["docs management"])

@router.get("/")
@inject
def get_all_docs():
    pass

@router.get("/id/{id}")
@inject
def get_docs_by_id():
    pass

@router.post("/")
@inject
def create_docs():
    pass

@router.put("/id/{id}")
@inject
def update_docs():
    pass

@router.delete("/id/{id}")
@inject
def delete_docs():
    pass