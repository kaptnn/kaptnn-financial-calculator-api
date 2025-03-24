from datetime import datetime
from typing import Union, TypedDict, Optional
from fastapi import HTTPException
from app.core.exceptions import InternalServerError
from app.models.company_model import Company
from app.models.profile_model import Profile 
from app.repositories.company_repo import CompanyRepository 
from app.services.base_service import BaseService

class CompanyDict(TypedDict):
    id: str
    company_name: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class CompanyService(BaseService):
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository
        super().__init__(company_repository)

    def get_companies(self, page: int, limit: int, sort: str, order: str):
        companies = self.company_repository.get_all_companies()

        if not companies:
            return {"results": [], "total_items": 0, "total_pages": 0}

        if sort not in companies[0]:
            raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort}")

        reverse = (order.lower() == "desc")
        companies_sorted = sorted(companies, key=lambda x: x.get(sort, ""), reverse=reverse)

        total_items = len(companies_sorted)
        total_pages = (total_items + limit - 1) // limit
        offset = (page - 1) * limit
        paginated_companies = companies_sorted[offset : offset + limit]

        return {
            "results": paginated_companies,
            "total_items": total_items,
            "total_pages": total_pages,
        }

    def get_company_by_options(self, option: str, value: Union[str, str]) -> CompanyDict:
        company: Optional[Company] = self.company_repository.get_company_by_options(option, value) or (None, None)

        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        return CompanyDict(
            id=company.id,
            company_name=company.company_name,
            created_at=company.created_at,
            updated_at=company.updated_at,
        )
        

    def create_company(self, company_name: str) -> CompanyDict:
        new_company = self.company_repository.create_company(company_name)

        if not new_company:
            raise InternalServerError("Failed to create company. Please try again later")

        result = CompanyDict(id=new_company.id,
            company_name=new_company.company_name,
            created_at=new_company.created_at,
            updated_at=new_company.updated_at,
        )

        return {"message": "Company successfully registered", "data": result }
    
    def update_company(self, id: str, company: dict) -> CompanyDict:
        existing_company = self.company_repository.get_company_by_options("id", id)
        
        if not existing_company:
            raise HTTPException(status_code=404, detail="Company not found")

        updated_company: Company = self.company_repository.update_company(id, company)

        return CompanyDict(
            id=updated_company.id,
            company_name=updated_company.company_name,
            created_at=updated_company.created_at,
            updated_at=updated_company.updated_at,
        )
    
    def delete_company(self, id: str):
        existing_company = self.company_repository.get_company_by_options("id", id)
        if not existing_company:
            raise HTTPException(status_code=404, detail="User not found")

        success = self.company_repository.delete_company(id)
        if not success:
            raise InternalServerError("Failed to delete company. Please try again later")

        return {"message": "Company deleted successfully"}

