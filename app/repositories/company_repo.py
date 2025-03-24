from sqlmodel import Session, select
from contextlib import AbstractContextManager
from typing import Callable, Optional, Union
from app.models.company_model import Company
from app.repositories.base_repo import BaseRepository

class CompanyRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Company)

    def get_all_companies(self):
        with self.session_factory() as session:
            statement = select(Company)
            result = session.exec(statement).all()
            
            data = [
                {
                    "id": company.id,
                    "company_name": company.company_name,
                    "created_at": company.created_at,
                    "updated_at": company.updated_at,
                }
                for company in result
            ]

            return data
        
    def get_company_by_options(self, option: str, value: Union[str, str]) -> Optional[Company]:
        if option not in ["id", "company_name"]:
            raise ValueError("Invalid option")

        with self.session_factory() as session:
            statement = select(Company).where(getattr(Company, option) == value)
            result = session.exec(statement).one_or_none()

            if result is None:
                return None

            session.expunge_all()
            return result
        
    def create_company(self, company_name: str) -> Company:
        with self.session_factory() as session:
            company = Company(id=None, company_name=company_name, created_at=None, updated_at=None)

            session.add(company)
            session.commit()
            session.refresh(company)

            session.expunge_all()
            return company
        
    def update_company(self, id: str, company: dict) -> Optional[Company]:
        with self.session_factory() as session:
            statement = select(Company).where(Company.id == id)
            result = session.exec(statement).one()

            if not result:
                return None
            
            for key, value in company.items():
                if hasattr(result, key):
                    setattr(result, key, value)

            session.add(result)
            session.commit()
            session.refresh(result)

            session.expunge_all()
            return result
        
    def delete_company(self, id: str):
        with self.session_factory() as session:
            statement = select(Company).where(Company.id == id)
            result = session.exec(statement).one()

            if not result:
                return False

            session.delete(result)
            session.commit()
            
            session.expunge_all()
            return True