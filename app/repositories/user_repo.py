from uuid import UUID
from sqlmodel import Session, func, select
from contextlib import AbstractContextManager
from typing import Any, Callable, Dict, Union, Optional
from app.models.user_model import User
from app.models.profile_model import Profile
from app.repositories.base_repo import BaseRepository
from app.schema.user_schema import DeleteUserResponse, FindAllUsersResponse, FindUserByOptionsResponse, UpdateUserProfileRequest, User as UserSchema, Profile as ProfileSchema, UpdateUserProfileResponse

class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, User)

    def get_all_users(
        self, 
        page: int = 1,
        limit: int = 100,
        sort: str = "created_at",
        order: str = "asc",
        filters: Optional[Dict[str, Any]] = None
    ) -> FindAllUsersResponse:
        with self.session_factory() as session:
            statement = select(User, Profile).join(Profile, isouter=True)

            if filters:
                if email := filters.get("email"):
                    statement = statement.where(User.email == email)
                if company_id := filters.get("company_id"):
                    statement = statement.where(User.company_id == company_id)
                if name_query := filters.get("name"):
                    statement = statement.where(User.name.ilike(f"%{name_query}%"))
            
            sort_column = getattr(User, sort)
            if order.lower() == "desc":
                sort_column = sort_column.desc()
            statement = statement.order_by(sort_column)

            total_items = session.exec(select(func.count()).select_from(statement.subquery())).one()
            total_pages = (total_items + limit - 1) // limit
            offset = (page - 1) * limit

            statement = statement.offset(offset).limit(limit)
            result = session.exec(statement).all()
            
            users_list = []
            for user_obj, profile_obj in result:
                setattr(user_obj, "profile", profile_obj)
                users_list.append(UserSchema.model_validate(user_obj))

            return FindAllUsersResponse(
                message="Success retrieved data from repository",
                result=users_list,
                meta={ 'current_page': page, "total_items": total_items, 'total_pages': total_pages }
            )
        
    def get_user_by_options(self, option: str, value: Union[str, UUID]) -> FindUserByOptionsResponse:
        with self.session_factory() as session:
            statement = select(User, Profile).join(Profile, isouter=True).where(getattr(User, option) == value)
            result = session.exec(statement).all()

            if option in ("id", "email"):
                if not result:
                    return FindUserByOptionsResponse(
                        message="No user found",
                        result=None,
                        meta=None,
                    )
                
                user_obj, profile_obj = result[0]
                setattr(user_obj, "profile", profile_obj)
                user_schema = UserSchema.model_validate(user_obj)
                return FindUserByOptionsResponse(
                    message="Success retrieved data from repository",
                    result=user_schema,
                    meta=None
                )
        
    def create_user(self, name: str, email: str, password: str, company_id: str) -> User:
        with self.session_factory() as session:
            user = User(name=name, email=email, password=password, company_id=company_id, id=None, created_at=None, updated_at=None)

            session.add(user)
            session.commit()
            session.refresh(user)

            session.expunge_all()
            return user
        
    def create_user_profile(self, user_id: str) -> Profile:
        with self.session_factory() as session:
            profile = Profile(user_id=user_id, id=None, created_at=None, updated_at=None)

            session.add(profile)
            session.commit()
            session.refresh(profile)

            session.expunge_all()
            return profile
        
    def update_user_profile(self, user_id: UUID, profile_info: UpdateUserProfileRequest) -> UpdateUserProfileResponse:
        with self.session_factory() as session:
            statement = select(Profile).where(Profile.user_id == user_id)
            profile = session.exec(statement).one()

            data = profile_info.model_dump(exclude_unset=True)
            for field, value in data.items():
                setattr(profile, field, value)
            
            session.add(profile)
            session.commit()
            session.refresh(profile)

            return UpdateUserProfileResponse(
                message="Success updated data from repository",
                result=ProfileSchema.model_validate(profile),
                meta=None
            )
        
    def delete_user(self, user_id: UUID) -> DeleteUserResponse:
        with self.session_factory() as session:
            user = session.get(User, user_id)
            if not user:
                return DeleteUserResponse(
                    message="User not found",
                    result=None,
                    meta=None
                )

            statement = select(Profile).where(Profile.user_id == user_id)
            profile = session.exec(statement).one()
            if profile:
                session.delete(profile)

            session.delete(user)
            session.commit()
            
            return DeleteUserResponse(
                message="Success deleted data from repository", 
                result=None, 
                meta=None
            )