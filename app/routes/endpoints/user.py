from typing import Any, Dict, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from dependency_injector.wiring import Provide
from app.core.container import Container
from app.core.middleware import inject
from app.core.dependencies import get_current_user
from app.schema.user_schema import DeleteUserResponse, FindAllUsersResponse, FindUserByOptionsResponse, UpdateUserProfileRequest, UpdateUserProfileResponse, User
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["User Management"])

@router.get("/", 
    response_model=FindAllUsersResponse, 
    status_code=status.HTTP_200_OK, 
    response_model_exclude={"result": {"__all__": {"password"}}}, 
    response_model_exclude_none=True)
@inject
def get_all_users(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of users per page"),
    sort: str = Query("created_at", description="Field to sort by"),
    order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order (asc or desc)"),
    email: Optional[str] = Query(None, description="Filter by exact email"),
    name: Optional[str] = Query(None, description="Filter by name substring"),
    company_id: Optional[UUID] = Query(None, description=""),
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user)
):
    filters: Dict[str, Any] = {}
    if email:
        filters["email"] = email
    if name:
        filters["name"] = name
    if company_id:
        filters["company_id"] = company_id
    
    users = service.get_all_users(
            page=page,
            limit=limit,
            sort=sort,
            order=order,
            filters=filters,
        )
    
    return {
        'message': "Users retrieved successfully", 
        'result': users.result, 
        'meta': {
            "current_page": page,
            "total_pages": users.meta.total_pages,
            "total_items": users.meta.total_items,
        }
    }

@router.get("/me", 
    response_model=FindUserByOptionsResponse, 
    status_code=status.HTTP_200_OK, 
    response_model_exclude={"result": {"password"}}, 
    response_model_exclude_none=True)
@inject
def get_current_user_data(
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user)
):
    return FindUserByOptionsResponse(
        message="Current user retrieved successfully",
        result=current_user,
        meta=None
    )

@router.put("/me/profile", 
    response_model=UpdateUserProfileResponse, 
    status_code=status.HTTP_200_OK, 
    response_model_exclude={"result": {"password"}}, 
    response_model_exclude_none=True)
@inject
def update_my_profile(
    profile_info: UpdateUserProfileRequest,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user),
):
    profile = service.attach_user_profile(current_user.id, profile_info)
    return UpdateUserProfileResponse(
        message="Profile attached successfully",
        result=profile.result,
        meta=None
    )

@router.get("/{user_id}", 
    response_model=FindUserByOptionsResponse, 
    status_code=status.HTTP_200_OK, 
    response_model_exclude={"result": {"password"}}, 
    response_model_exclude_none=True)
@inject
def get_user_by_id(
    user_id: UUID,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user),
):
    user = service.get_user_by_options(option="id", value=user_id)
    return FindUserByOptionsResponse(
        message="User retrieved successfully",
        result=user.result,
        meta=None
    )

@router.put("/{user_id}", 
    response_model=UpdateUserProfileResponse, 
    status_code=status.HTTP_200_OK, 
    response_model_exclude={"result": {"password"}}, 
    response_model_exclude_none=True)
@inject
def get_user_by_id(
    user_id: UUID,
    profile_info: UpdateUserProfileRequest,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user),
):
    user = service.get_user_by_options(option="id", value=user_id)
    profile = service.attach_user_profile(user.result.id, profile_info)
    return UpdateUserProfileResponse(
        message="Profile attached successfully",
        result=profile.result,
        meta=None
    )

@router.delete("/{user_id}", 
    response_model=DeleteUserResponse, 
    status_code=status.HTTP_200_OK, 
    response_model_exclude={"result": {"password"}}, 
    response_model_exclude_none=True)
@inject
def delete_user(
    user_id: UUID,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user)
):
    service.delete_user(user_id)
    return DeleteUserResponse(
        message='User deleted successfully',
        result=None,
        meta=None
    )
    