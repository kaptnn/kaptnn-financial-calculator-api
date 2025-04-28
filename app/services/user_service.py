from uuid import UUID 
from datetime import datetime
from typing import Any, Dict, List, Union, Optional
from fastapi import HTTPException
from app.core.exceptions import InternalServerError
from app.repositories.user_repo import UserRepository 
from app.schema.user_schema import DeleteUserResponse, FindAllUsersResponse, FindUserByOptionsResponse, User, Profile, UpdateUserProfileRequest, UpdateUserProfileResponse
from app.services.base_service import BaseService

class UserService(BaseService):
    ALLOWED_SORTS = {"id", "email", "name", "created_at"}
    ALLOWED_ORDERS = {"asc", "desc"}
    ALLOWED_FILTERS = {"id", "email", "name", "company_id"}

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def get_all_users(
        self, 
        page: int = 1, 
        limit: int = 100, 
        sort: str = "created_at", 
        order: str = "asc", 
        filters: Optional[Dict[str, Any]] = None
    ) -> FindAllUsersResponse:
        if page < 1:
            page = 1
        if not (1 <= limit <= 100):
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
        
        if sort not in self.ALLOWED_SORTS:
            raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort!r}. Must be one of {self.ALLOWED_SORTS}")

        order = order.lower()
        if order not in self.ALLOWED_ORDERS:
            raise HTTPException(status_code=400, detail=f"Invalid order: {order!r}. Must be one of {self.ALLOWED_ORDERS}")
        
        if filters is not None:
            invalid_keys = set(filters.keys()) - self.ALLOWED_FILTERS
            if invalid_keys:
                raise HTTPException(status_code=400, detail=f"Invalid filter keys: {invalid_keys}. Allowed filters are {self.ALLOWED_FILTERS}")

        return self.user_repository.get_all_users(
            page=page,
            limit=limit,
            sort=sort,
            order=order,
            filters=filters,
        )

    def get_user_by_options(
        self, 
        option: str, 
        value: Union[str, UUID]
    ) -> FindUserByOptionsResponse:
        if option not in self.ALLOWED_FILTERS:
            raise HTTPException(status_code=400, detail="Invalid option field")
        
        response = self.user_repository.get_user_by_options(option, value)

        if response.result is None:
            raise HTTPException(status_code=404, detail="User not found")

        return response
    
    def delete_user(self, user_id: UUID) -> DeleteUserResponse:
        existing_user = self.user_repository.get_user_by_options("id", user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        response = self.user_repository.delete_user(user_id)
        if not response:
            raise InternalServerError("Failed to delete user. Please try again later")

        return response

    def attach_user_profile(self, user_id: UUID, profile_info: UpdateUserProfileRequest) -> UpdateUserProfileResponse:
        existing_user = self.user_repository.get_user_by_options("id", user_id)
        if existing_user.result is None:
            raise HTTPException(status_code=404, detail="User not found")

        response = self.user_repository.update_user_profile(user_id, profile_info)
        if not response:
            raise InternalServerError("Failed to update user. Please try again later")

        return response
