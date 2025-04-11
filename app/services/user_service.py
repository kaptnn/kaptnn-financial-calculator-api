import uuid 
from datetime import datetime
from typing import List, Union, TypedDict, Optional
from fastapi import HTTPException
from app.core.exceptions import InternalServerError
from app.models.profile_model import Profile 
from app.repositories.user_repo import UserRepository 
from app.schema.user_schema import DeleteUserResponse
from app.services.base_service import BaseService

class UserDict(TypedDict):
    id: str
    name: str
    email: str
    company_id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class UserProfileDict(TypedDict):
    id: str
    user_id: int
    role: str
    membership: str
    is_verified: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def get_all_users(self, page: int, limit: int, sort: str, order: str) -> dict:
        users = self.user_repository.get_all_users()

        if sort in users[0]:
            reverse = True if order == "desc" else False
            users = sorted(users, key=lambda x: x.get(sort, ""), reverse=reverse)
        else:
            raise ValueError(f"Invalid sort field: {sort}")

        total_items = len(users)
        total_pages = (total_items + limit - 1) // limit
        offset = (page - 1) * limit
        paginated_users = users[offset : offset + limit]

        return {
            "result": paginated_users,
            "total_items": total_items,
            "total_pages": total_pages,
        }

    def get_user_by_options(self, option: str, value: Union[str, int, uuid.UUID]) -> Union[UserDict, List[UserDict]]:
        result = self.user_repository.get_user_by_options(option, value)

        if result is None:
            raise HTTPException(status_code=404, detail="User not found")

        if option in ["id", "email"]:
            user, profile = result
            return UserDict(
                id=user.id or 0,
                name=user.name,
                email=user.email,
                company_id=user.company_id,
                created_at=user.created_at,
                updated_at=user.updated_at,
                profile=UserProfileDict(
                    id=profile.id,
                    user_id=profile.user_id,
                    role=profile.role,
                    membership=profile.membership_status,
                    is_verified=profile.is_verified,
                    created_at=profile.created_at,
                    updated_at=profile.updated_at
                ) if profile else None
            )
        elif option == "company_id":
            users = []
            for user, profile in result:
                users.append(
                    UserDict(
                        id=user.id or 0,
                        name=user.name,
                        email=user.email,
                        company_id=user.company_id,
                        created_at=user.created_at,
                        updated_at=user.updated_at,
                        profile=UserProfileDict(
                            id=profile.id,
                            user_id=profile.user_id,
                            role=profile.role,
                            membership=profile.membership_status,
                            is_verified=profile.is_verified,
                            created_at=profile.created_at,
                            updated_at=profile.updated_at
                        ) if profile else None
                    )
                )
            return users

    def attach_user_profile(self, user_id: str, profile_info: dict) -> Profile:
        user = self.user_repository.get_user_by_options("id", user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        profile = self.user_repository.update_user_profile(
            user_id=user_id,
            profile=Profile(**profile_info.model_dump())
        )
        return profile
    
    def delete_user(self, user_id: str) -> DeleteUserResponse:
        existing_user = self.user_repository.get_user_by_options("id", user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        success = self.user_repository.delete_user(user_id)
        if not success:
            raise InternalServerError("Failed to delete company. Please try again later")

        return {"message": "Company deleted successfully"}
