from uuid import UUID
from datetime import datetime
from sqlmodel import Session, func, select
from contextlib import AbstractContextManager
from typing import Any, Callable, Dict, Optional, Union
from app.models.company_model import Company
from app.models.user_model import User
from app.repositories.base_repo import BaseRepository
from app.core.config import configs
from app.schema.company_schema import DeleteCompanyResponse, FindAllCompaniesResponse, Company as CompanySchema, FindCompanyByOptionsResponse, UpdateCompanyRequest, UpdateCompanyResponse

class CompanyRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Company)

    def get_all_companies(
        self,
        page: int = 1,
        limit: int = 100,
        sort: str = "created_at",
        order: str = "asc",
        filters: Optional[Dict[str, Any]] = None
    ) -> FindAllCompaniesResponse:
        with self.session_factory() as session:
            statement = select(Company).where(Company.company_name != configs.SUPER_ADMIN_COMPANY_NAME)
            
            if filters:
                if year_of_assignment := filters.get("year_of_assignment"):
                    statement = statement.where(Company.year_of_assignment == int(year_of_assignment))
                if name_query := filters.get("name"):
                    statement = statement.where(Company.company_name.ilike(f"%{name_query}%"))

            sort_column = getattr(Company, sort)
            if order.lower() == "desc":
                sort_column = sort_column.desc()
            statement = statement.order_by(sort_column)

            total_items = session.exec(select(func.count()).select_from(statement.subquery())).one()
            total_pages = (total_items + limit - 1) // limit
            offset = (page - 1) * limit

            statement = statement.offset(offset).limit(limit)
            result = session.exec(statement).all()

            companies_list = [CompanySchema.model_validate(c) for c in result]
            
            return FindAllCompaniesResponse(
                message="Success retrieved data from repository",
                result=companies_list,
                meta={ 'current_page': page, "total_items": total_items, 'total_pages': total_pages }
            )
        
    def get_company_by_options(self, option: str, value: Union[str, UUID]) -> FindCompanyByOptionsResponse:
        with self.session_factory() as session:
            statement = select(Company).where(getattr(Company, option) == value)
            result = session.exec(statement).all()

            if option in ("id", "company_name"):
                if not result:
                    return FindCompanyByOptionsResponse(
                        message="No company found",
                        result=None,
                        meta=None,
                    )

                company_obj = result[0]
                company_schema = CompanySchema.model_validate(company_obj)
                return FindCompanyByOptionsResponse(
                    message="Success retrieved data from repository",
                    result=company_schema,
                    meta=None
                )
            
    def create_company(self, company_name: str, year_of_assignment: int, start_audit_period: datetime, end_audit_period=datetime) -> Company:
        with self.session_factory() as session:
            company = Company(company_name=company_name, year_of_assignment=year_of_assignment, start_audit_period=start_audit_period, end_audit_period=end_audit_period)

            session.add(company)
            session.commit()
            session.refresh(company)

            session.expunge_all()
            return company
        
    def update_company(self, company_id: UUID, company_info: UpdateCompanyRequest) -> UpdateCompanyResponse:
        with self.session_factory() as session:
            statement = select(Company).where(Company.id == company_id)
            company = session.exec(statement).one()
            
            data = company_info.model_dump(exclude_unset=True)
            for field, value, in data.items():
                setattr(company, field, value)

            session.add(company)
            session.commit()
            session.refresh(company)

            CompanySchema.model_validate(company)

            return UpdateCompanyResponse(
                message="Success updated data from repository",
                result=None,
                meta=None
            )
        
    def delete_company(self, company_id: UUID) -> DeleteCompanyResponse:
        with self.session_factory() as session:
            company = session.get(Company, company_id)

            if not company:
                return DeleteCompanyResponse(
                    message="Company not found",
                    result=None,
                    meta=None
                )

            session.delete(company)
            session.commit()
            
            return DeleteCompanyResponse(
                message="Success deleted data from repository",
                result=None,
                meta=None
            )
        
    def company_user_count(self):
        with self.session_factory() as session:
            user_count = func.count(User.id).label("user_count")

            stmt = (
                select(
                    Company.company_name.label("name"),
                    user_count.label("total")
                )
                .select_from(Company)
                .join(User, Company.id == User.company_id, isouter=True)
                .where(Company.company_name != "Super Admin Company")
                .group_by(Company.id, Company.company_name)
                .having(user_count > 0)
                .order_by(user_count.desc())
            )

            results = session.exec(stmt).all()

            return [
                {"name": row.name, "total": row.total}
                for row in results
            ]