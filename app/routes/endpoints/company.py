import uuid
from fastapi import APIRouter, Depends, Query, status
from dependency_injector.wiring import Provide
from app.core.container import Container
from app.core.middleware import inject
from app.core.dependencies import get_current_user
from app.schema.company_schema import FindCompanyByOptionsResponse, CreateCompanyRequest, CreateCompanyResponse, UpdateCompanyRequest, UpdateCompanyResponse, DeleteCompanyResponse
from app.services.company_service import CompanyService
from app.services.user_service import UserDict

router = APIRouter(prefix="/companies", tags=["Company"])

@router.get("/", response_model=dict, status_code=status.HTTP_200_OK)
@inject
def get_all_companies(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(5, ge=1, le=100, description="Number of users per page"),
    sort: str = Query("created_at", description="Field to sort by"),
    order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order (asc or desc)"),
    service: CompanyService = Depends(Provide[Container.company_service]),
):
    companies = service.get_all_companies(page=page, limit=limit, sort=sort, order=order)
    return {
        "message": "Companies retrieved successfully",
        "result": companies["result"],
        "pagination": {
            "current_page": page,
            "total_pages": companies["total_pages"],
            "total_items": companies["total_items"],
        },
    }

@router.get("/{company_id}", response_model=FindCompanyByOptionsResponse, status_code=status.HTTP_200_OK)
@inject
def get_company_by_id(
    id: uuid.UUID,
    service: CompanyService = Depends(Provide[Container.company_service]),
    current_user: UserDict = Depends(get_current_user),
):
    result = service.get_company_by_options(option="id", value=id)
    return {
        "message": "Company retrieved successfully",
        "result": result,
    }

@router.post("/", response_model=CreateCompanyResponse, status_code=status.HTTP_201_CREATED)
@inject
def create_company(
    company: CreateCompanyRequest,
    service: CompanyService = Depends(Provide[Container.company_service]),
    current_user: UserDict = Depends(get_current_user),
):
    return service.create_company(company)

# UN-TESTED
# CURRENT ERROR: THE FIELD NOT OPTIONALLY SO ALL FIELD STILL REQUIRED
@router.put("/{company_id}", response_model=UpdateCompanyResponse, status_code=status.HTTP_200_OK)
@inject
def update_company(
    company: UpdateCompanyRequest,
    service: CompanyService = Depends(Provide[Container.company_service]),
    current_user: UserDict = Depends(get_current_user),
):
    result = service.update_company(id, company)
    return {
        "message": "Company updated successfully",
        "result": result,
    }

# UN-TESTED
# CURRENT ERROR: I THINK IT SHOULD BE NEED TO DELETE THE USER IN THE COMPANY
#                ID SHOULD BE HEX OR UUID
@router.delete("/{company_id}", response_model=DeleteCompanyResponse, status_code=status.HTTP_200_OK)
@inject
def delete_company(
    service: CompanyService = Depends(Provide[Container.company_service]),
    current_user: UserDict = Depends(get_current_user),
):
    return service.delete_company(id)