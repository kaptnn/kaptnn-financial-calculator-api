import uuid
from datetime import datetime
from typing import List, TypedDict, Optional, Union
from fastapi import HTTPException
from app.core.exceptions import InternalServerError
from app.repositories.company_repo import CompanyRepository 
from app.schema.company_schema import CreateCompanyRequest, CreateCompanyResponse, Company, UpdateCompanyRequest, UpdateCompanyResponse, DeleteCompanyResponse, FindCompanyByOptionsResponse
from app.services.base_service import BaseService

class CompanyDict(TypedDict):
    id: str
    company_name: str
    year_of_assignment: int
    start_audit_period: datetime 
    end_audit_period: datetime
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class CompanyService(BaseService):
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository
        super().__init__(company_repository)

    def get_all_companies(self, page: int, limit: int, sort: str, order: str) -> dict:
        companies = self.company_repository.get_all_companies()

        if not companies:
            return {"result": [], "total_items": 0, "total_pages": 0}

        if sort not in companies[0]:
            raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort}")

        reverse = (order.lower() == "desc")
        companies_sorted = sorted(companies, key=lambda x: x.get(sort, ""), reverse=reverse)

        total_items = len(companies_sorted)
        total_pages = (total_items + limit - 1) // limit
        offset = (page - 1) * limit
        paginated_companies = companies_sorted[offset : offset + limit]

        return {
            "result": paginated_companies,
            "total_items": total_items,
            "total_pages": total_pages,
        }

    def get_company_by_options(self, option: str, value: Union[str, uuid.UUID]) -> Optional[Union[CompanyDict, List[CompanyDict]]]:
        result = self.company_repository.get_company_by_options(option, value)

        if not result:
            raise HTTPException(status_code=404, detail="Company not found")

        if option == "id":
            company = result
            company_dict = CompanyDict(
                id=str(company.id),
                company_name=company.company_name,
                year_of_assignment=company.year_of_assignment,
                start_audit_period=company.start_audit_period,
                end_audit_period=company.end_audit_period,
                created_at=company.created_at,
                updated_at=company.updated_at,
            )
            return company_dict

        elif option == "company_name":
            companies = []
            for company in result:
                companies.append(
                    CompanyDict(
                        id=str(company.id), 
                        company_name=company.company_name,
                        year_of_assignment=company.year_of_assignment,
                        start_audit_period=company.start_audit_period,
                        end_audit_period=company.end_audit_period,
                        created_at=company.created_at,
                        updated_at=company.updated_at,
                    )
                )
            return companies

    def create_company(self, company: CreateCompanyRequest) -> CreateCompanyResponse:
        new_company = self.company_repository.create_company(
            company_name=company.company_name,
            year_of_assignment=company.year_of_assignment,
            start_audit_period=company.start_audit_period,
            end_audit_period=company.end_audit_period
        )

        if not new_company:
            raise InternalServerError("Failed to create company. Please try again later")

        result = Company(
            id=str(new_company.id),
            company_name=new_company.company_name,
            year_of_assignment=new_company.year_of_assignment, 
            start_audit_period=new_company.start_audit_period, 
            end_audit_period=new_company.end_audit_period,
            created_at=new_company.created_at,
            updated_at=new_company.updated_at,
        )

        return CreateCompanyResponse(
            message="Company successfully registered", 
            result=result.model_dump()
        )


    def update_company(self, company_id: str, company: UpdateCompanyRequest) -> UpdateCompanyResponse:
        existing_company = self.company_repository.get_company_by_options("id", company_id)
        
        if not existing_company:
            raise HTTPException(status_code=404, detail="Company not found")

        updated_company = self.company_repository.update_company(company_id, company)

        return Company(
            id=updated_company.id,
            company_name=updated_company.company_name,
            year_of_assignment=updated_company.year_of_assignment, 
            start_audit_period=updated_company.start_audit_period, 
            end_audit_period=updated_company.end_audit_period,
            created_at=updated_company.created_at,
            updated_at=updated_company.updated_at,
        )


    def delete_company(self, company_id: str) -> DeleteCompanyResponse:
        existing_company = self.company_repository.get_company_by_options("id", company_id)
        if not existing_company:
            raise HTTPException(status_code=404, detail="User not found")

        success = self.company_repository.delete_company(company_id)
        if not success:
            raise InternalServerError("Failed to delete company. Please try again later")
        
        # it should delete the folder in one drive

        return {"message": "Company deleted successfully"}

