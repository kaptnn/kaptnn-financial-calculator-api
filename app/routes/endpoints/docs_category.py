from fastapi import APIRouter
from app.core.middleware import inject

router = APIRouter(prefix="/docs-category", tags=["docs categories"])

@router.get("/")
@inject
def get_all_docs_categories():
    pass

@router.get("/id/{id}")
@inject
def get_docs_category_by_id():
    pass

@router.post("/")
@inject
def create_docs_category():
    pass

@router.put("/id/{id}")
@inject
def update_docs_category():
    pass

@router.delete("/id/{id}")
@inject
def delete_docs_category():
    pass