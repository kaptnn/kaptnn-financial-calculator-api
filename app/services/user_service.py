from datetime import datetime
from typing import Union, TypedDict, Optional
from fastapi import HTTPException
from sqlmodel import asc, desc
from app.models.profile_model import Profile 
from app.models.user_model import User
from app.repositories.user_repo import UserRepository 
from app.services.base_service import BaseService

class UserDict(TypedDict):
    id: int
    name: str
    email: str
    password: str
    company_id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class UserProfileDict(TypedDict):
    id: int
    user_id: int
    role: str
    membership: str
    is_verified: bool
    created_at: datetime | None
    updated_at: datetime | None

class UserService(BaseService):
    async def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    async def get_users(self, page: int, limit: int, sort: str, order: str):
        users = self.user_repository.get_users()

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
            "results": paginated_users,
            "total_items": total_items,
            "total_pages": total_pages,
        }

    async def get_user_by_options(self, option: str, value: Union[str, int]) -> UserDict:
        user, profile = self.user_repository.get_user_by_options(option, value) or (None, None)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

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

    async def attach_user_profile(self, user_id: int, profile_info: dict) -> Profile:
        user = self.user_repository.get_user_by_options("id", user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        profile = self.user_repository.update_user_profile(
            user_id=user_id,
            profile=Profile(**profile_info.model_dump())
        )
        return profile
