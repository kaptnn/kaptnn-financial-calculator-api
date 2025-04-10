import uuid
from fastapi import APIRouter, Depends, Query
from dependency_injector.wiring import Provide
from app.core.container import Container
from app.core.middleware import inject
from app.core.dependencies import get_current_user
from app.schema.company_schema import CreateCompanySchema
from app.services.company_service import CompanyService
from app.services.user_service import UserDict

router = APIRouter(prefix="/companies", tags=["company"])

@router.get("/")
@inject
def get_all_companies(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(5, ge=1, le=100, description="Number of users per page"),
    sort: str = Query("created_at", description="Field to sort by"),
    order: str = Query("asc", regex="^(asc|desc)$", description="Sort order (asc or desc)"),
    service: CompanyService = Depends(Provide[Container.company_service]),
):
    companies = service.get_companies(page=page, limit=limit, sort=sort, order=order)
    return {
        "message": "Companies retrieved successfully",
        "data": companies["results"],
        "pagination": {
            "current_page": page,
            "total_pages": companies["total_pages"],
            "total_items": companies["total_items"],
        },
    }

@router.get("/company/id/{id}")
@inject
def get_company_by_id(
    id: uuid.UUID,
    service: CompanyService = Depends(Provide[Container.company_service]),
    current_user: UserDict = Depends(get_current_user),
):
    company = service.get_company_by_options(option="id", value=id)
    return {
        "message": "Company retrieved successfully",
        "data": company,
    }

@router.get("/company/email/{email}")
@inject
def get_company_by_email(
    email: str,
    service: CompanyService = Depends(Provide[Container.company_service]),
    current_user: UserDict = Depends(get_current_user),
):
    company = service.get_company_by_options(option="email", value=email)
    return {
        "message": "Company retrieved successfully",
        "data": company,
    }

@router.post("/")
@inject
def create_company(
    company: CreateCompanySchema,
    service: CompanyService = Depends(Provide[Container.company_service]),
):
    company = service.create_company(company.company_name)
    return {
        "message": "Company successfully registered",
        "data": company,
    }

@router.put("/company/id/{id}")
@inject
def update_company(
    company: dict,
    service: CompanyService = Depends(Provide[Container.company_service]),
    current_user: UserDict = Depends(get_current_user),
):
    company = service.update_company(id, company)
    return {
        "message": "Company updated successfully",
        "data": company,
    }

@router.delete("/company/id/{id}")
@inject
def delete_company(
    service: CompanyService = Depends(Provide[Container.company_service]),
    current_user: UserDict = Depends(get_current_user),
):
    return service.delete_company(id)