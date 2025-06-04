from datetime import datetime
import os
from uuid import UUID
from typing import Any, Dict, Optional, Union
from fastapi import HTTPException, status
from app.core.exceptions import InternalServerError
from app.repositories.company_repo import CompanyRepository 
from app.schema.company_schema import CreateCompanyRequest, CreateCompanyResponse, Company, FindAllCompaniesResponse, UpdateCompanyRequest, UpdateCompanyResponse, DeleteCompanyResponse, FindCompanyByOptionsResponse
from app.services.base_service import BaseService
from app.core.config import configs
from app.utils.helpers import make_safe_onedrive_folder_name

class CompanyService(BaseService):
    ALLOWED_SORTS = {"id", "company_name", "created_at"}
    ALLOWED_ORDERS = {"asc", "desc"}
    ALLOWED_FILTERS = {"id", "name", "year_of_assignment"}

    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository
        super().__init__(company_repository)

    def get_all_companies(
        self, 
        page: int = 1, 
        limit: int = 100, 
        sort: str = "created_at", 
        order: str = "asc",
        filters: Optional[Dict[str, Any]] = None
    ) -> FindAllCompaniesResponse:
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

        return self.company_repository.get_all_companies(
            page=page,
            limit=limit,
            sort=sort,
            order=order,
            filters=filters
        )

    def get_company_by_options(
        self, 
        option: str, 
        value: Union[str, UUID]
    ) -> FindCompanyByOptionsResponse:
        if option not in self.ALLOWED_FILTERS:
            raise HTTPException(status_code=400, detail="Invalid option field")
        
        response = self.company_repository.get_company_by_options(option, value)

        if response.result is None:
            raise HTTPException(status_code=404, detail="Company not found")

        return response

    def create_company(self, company: CreateCompanyRequest) -> CreateCompanyResponse:
        current_year = datetime.now().year
        if company.year_of_assignment > current_year:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Year of assignment cannot be in the future."
            )

        if company.start_audit_period > company.end_audit_period:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Audit period start date cannot be after end date."
            )

        if (company.start_audit_period.year != company.year_of_assignment):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Audit period dates must fall within the year of assignment."
            )
        
        existing_company = self.company_repository.get_company_by_options("company_name", company.company_name)
        if existing_company.result is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A company with this name is already registered."
            )

        new_company = self.company_repository.create_company(
            company_name=company.company_name,
            year_of_assignment=company.year_of_assignment,
            start_audit_period=company.start_audit_period,
            end_audit_period=company.end_audit_period
        )

        safe_name = make_safe_onedrive_folder_name(company.company_name)
        os.makedirs(f"{configs.UPLOAD_DIR_ROOT}/{safe_name}", exist_ok=True)

        if not new_company:
            raise InternalServerError("Failed to create company. Please try again later")

        return CreateCompanyResponse(
            message="Company successfully registered", 
            result=None,
            meta=None,
        )

    def update_company(self, company_id: UUID, company_info: UpdateCompanyRequest) -> UpdateCompanyResponse:
        existing_company = self.company_repository.get_company_by_options("id", company_id)
        
        if existing_company.result is None:
            raise HTTPException(status_code=404, detail="Company not found")

        current_year = datetime.now().year
        if company_info.year_of_assignment > current_year:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Year of assignment cannot be in the future."
            )

        if company_info.start_audit_period > company_info.end_audit_period:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Audit period start date cannot be after end date."
            )

        if (company_info.start_audit_period.year != company_info.year_of_assignment):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Audit period dates must fall within the year of assignment."
            )

        response = self.company_repository.update_company(company_id, company_info)

        if not response:
            raise InternalServerError("Failed to update user. Please try again later")

        return response

    def delete_company(self, company_id: UUID) -> DeleteCompanyResponse:
        existing_company = self.company_repository.get_company_by_options("id", company_id)
        if not existing_company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

        response = self.company_repository.delete_company(company_id)
        if not response:
            raise InternalServerError("Failed to delete company. Please try again later")
        
        return response
