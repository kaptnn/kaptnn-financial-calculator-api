import uuid
from sqlmodel import Session, select
from contextlib import AbstractContextManager
from typing import Callable, List, Union, Optional, Tuple
from app.models.user_model import User
from app.models.profile_model import Profile
from app.repositories.base_repo import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, User)

    def get_all_users(self) -> List[User]:
        with self.session_factory() as session:
            statement = select(User, Profile).join(Profile, isouter=True)
            result = session.exec(statement).all()
            
            data = [
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "company_id": user.company_id,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at,
                    "profile": {
                        "id": profile.id,
                        "user_id": profile.user_id,
                        "role": profile.role,
                        "membership": profile.membership_status,
                        "is_verified": profile.is_verified,
                        "created_at": profile.created_at,
                        "updated_at": profile.updated_at,
                    }
                }
                for user, profile in result
            ]

            return data
        
    def get_user_by_options(self, option: str, value: Union[str, int, uuid.UUID]) -> Optional[Union[Tuple[User, Profile], List[Tuple[User, Profile]]]]:
        if option not in ["id", "email", "company_id"]:
            raise ValueError("Invalid option")

        with self.session_factory() as session:
            statement = select(User, Profile).join(Profile, isouter=True).where(getattr(User, option) == value)
            results = session.exec(statement).all()

            if results is None:
                return None
            
            session.expunge_all()
            
            if option in ["id", "email"]:
                return results[0] if results else None
            elif option == "company_id":
                return results
        
    def create_user(self, name: str, email: str, password: str, company_id: str) -> User:
        with self.session_factory() as session:
            user = User(name=name, email=email, password=password, company_id=company_id, id=None, created_at=None, updated_at=None)

            session.add(user)
            session.commit()
            session.refresh(user)

            session.expunge_all()
            return user
        
    def create_user_profile(self, profile: Profile) -> Profile:
        with self.session_factory() as session:
            session.add(profile)
            session.commit()
            session.refresh(profile)

            session.expunge_all()
            return profile
        
    def update_user_profile(self, user_id: int, profile: Profile) -> Profile:
        with self.session_factory() as session:
            statement = select(Profile).where(Profile.user_id == user_id)
            result = session.exec(statement).one()

            result = result.model_copy(update=profile.model_dump(exclude_unset=True))

            result = session.merge(result)
            session.commit()
            session.refresh(result)

            session.expunge_all()
            return result
        
    def delete_user(self, id: str) -> bool:
        with self.session_factory() as session:
            statement = select(User).where(User.id == id)
            result = session.exec(statement).one()

            if not result:
                return False

            session.delete(result)
            session.commit()
            
            session.expunge_all()
            return True