from sqlmodel import Session, select
from contextlib import AbstractContextManager
from typing import Callable, Union, Optional, Tuple
from app.models.user_model import User
from app.models.company_model import Company
from app.models.profile_model import Profile
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
                    "company_name": company.name,
                    "created_at": company.created_at,
                    "updated_at": company.updated_at,
                }
                for company in result
            ]

            return data
        
    def get_company_by_options(self, option: str, value: Union[str, int]) -> Optional[Tuple[User, Profile]]:
        if option not in ["id"]:
            raise ValueError("Invalid option")

        with self.session_factory() as session:
            statement = select(Company)
            result = session.exec(statement).one_or_none()

            if result is None:
                return None
            
            company = result

            session.expunge_all()
            return company
        
    def create_company(self, name: str, email: str, password: str) -> User:
        with self.session_factory() as session:
            user = User(name=name, email=email, password=password, id=None, created_at=None, updated_at=None)

            session.add(user)
            session.commit()
            session.refresh(user)

            session.expunge_all()
            return user
        
    def update_company(self, user_id: int, profile: Profile) -> Profile:
        with self.session_factory() as session:
            statement = select(Profile).where(Profile.user_id == user_id)
            result = session.exec(statement).one()

            result = result.model_copy(update=profile.model_dump(exclude_unset=True))

            result = session.merge(result)
            session.commit()
            session.refresh(result)

            session.expunge_all()
            return result
        
    def delete_company(self):
        pass