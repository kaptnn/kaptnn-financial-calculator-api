from typing import Any, Dict, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from dependency_injector.wiring import Provide
from app.core.container import Container
from app.core.middleware import inject
from app.core.dependencies import get_current_user
from app.schema.company_schema import FindAllCompaniesResponse, FindCompanyByOptionsResponse, CreateCompanyRequest, CreateCompanyResponse, UpdateCompanyRequest, UpdateCompanyResponse, DeleteCompanyResponse
from app.schema.user_schema import User
from app.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["Company"])

@router.get("/", 
    response_model=FindAllCompaniesResponse, 
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True)
@inject
def get_all_companies(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of users per page"),
    sort: str = Query("created_at", description="Field to sort by"),
    order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order (asc or desc)"),
    year_of_assignment: Optional[int] = Query(None, description="Filter by exact year of assignment"),
    name: Optional[str] = Query(None, description="Filter by name substring"),
    service: CompanyService = Depends(Provide[Container.company_service]),
):
    filters: Dict[str, Any] = {}
    if year_of_assignment:
        filters["year_of_assignment"] = int(year_of_assignment)
    if name:
        filters["name"] = name
        
    companies = service.get_all_companies(
                page=page, 
                limit=limit, 
                sort=sort, 
                order=order,
                filters=filters
            )
    
    return {
        "message": "Companies retrieved successfully",
        "result": companies.result,
        "meta": {
            "current_page": page,
            "total_pages": companies.meta.total_pages,
            "total_items": companies.meta.total_items,
        },
    }

@router.get("/summary/user", 
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True)
@inject
def get_company_user_count(
    service: CompanyService = Depends(Provide[Container.company_service]),
    current_user: User = Depends(get_current_user),
):
    
    summary = service.get_company_user_count()
    return {
        "message": "Company summary retrieved successfully",
        "result": summary,
        "meta": None,
    }

@router.get("/me", 
    response_model=FindCompanyByOptionsResponse, 
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True)
@inject
def get_company_by_current_user(
    service: CompanyService = Depends(Provide[Container.company_service]),
    current_user: User = Depends(get_current_user),
):
    
    company = service.get_company_by_options("id", current_user.company_id)
    return FindCompanyByOptionsResponse(
        message="Company retrieved successfully",
        result=company.result,
        meta=None,
    )

@router.get("/{company_id}", 
    response_model=FindCompanyByOptionsResponse, 
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True)
@inject
def get_company_by_id(
    company_id: UUID,
    service: CompanyService = Depends(Provide[Container.company_service]),
    current_user = Depends(get_current_user),
):
    company = service.get_company_by_options("id", company_id)
    return FindCompanyByOptionsResponse(
        message="Company retrieved successfully",
        result=company.result,
        meta=None,
    )

@router.post("/", 
    response_model=CreateCompanyResponse, 
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True)
@inject
def create_company(
    company: CreateCompanyRequest,
    service: CompanyService = Depends(Provide[Container.company_service]),
    current_user = Depends(get_current_user),
):
    return service.create_company(company)

@router.put("/{company_id}", 
    response_model=UpdateCompanyResponse, 
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True)
@inject
def update_company(
    company_id: UUID,
    company_info: UpdateCompanyRequest,
    service: CompanyService = Depends(Provide[Container.company_service]),
    current_user = Depends(get_current_user),
):
    company = service.update_company(company_id, company_info)
    return UpdateCompanyResponse(
        message="Company updated successfully",
        result=company.result,
        meta=None
    )

@router.delete("/{company_id}", 
    response_model=DeleteCompanyResponse, 
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True)
@inject
def delete_company(
    company_id: UUID,
    service: CompanyService = Depends(Provide[Container.company_service]),
    current_user = Depends(get_current_user),
):
    service.delete_company(company_id)
    return DeleteCompanyResponse(
        message='Company deleted successfully',
        result=None,
        meta=None
    )