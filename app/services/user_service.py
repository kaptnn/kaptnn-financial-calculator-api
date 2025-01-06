from datetime import datetime
from typing import Any, Union, TypedDict, Optional
from fastapi import HTTPException
from app.models.profile_model import Profile 
from app.repositories.user_repo import UserRepository 
from app.services.base_service import BaseService

class UserDict(TypedDict):
    id: int
    name: str
    email: str
    password: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class UserProfileDict(TypedDict):
    id: int
    user_id: int
    company: str
    membership: str
    created_at: datetime | None
    updated_at: datetime | None

class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def get_users(self) -> dict[str, Any]:
        data = self.user_repository.get_users()
        return {
            "data": data,
            "message": "Users retrieved successfully"
        }

    def get_user_by_options(self, option: str, value: Union[str, int]) -> UserDict:
        user, profile = self.user_repository.get_user_by_options(option, value) or (None, None)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return UserDict(
            id=user.id or 0,
            name=user.name,
            email=user.email,
            password=user.password,
            created_at=user.created_at,
            updated_at=user.updated_at,
            profile=UserProfileDict(
                id=profile.id,
                user_id=profile.user_id,
                company=profile.company if profile.company else "",
                membership=profile.membership_status,
                created_at=profile.created_at,
                updated_at=profile.updated_at
            ) if profile else None
        )

    def attach_user_profile(self, user_id: int, profile_info) -> Profile:
        user = self.user_repository.get_user_by_options("id", user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        profile = self.user_repository.update_user_profile(
            user_id=user_id,
            profile=Profile(**profile_info.model_dump())
        )
        return profile
