import uuid
from fastapi import APIRouter, Depends, Query, status
from dependency_injector.wiring import Provide
from app.core.container import Container
from app.core.middleware import inject
from app.core.dependencies import get_current_user
from app.schema.user_schema import DeleteUserResponse, FindUserByOptionsResponse, UpdateUserProfileResponse, User
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["User Management"])

@router.get("/", response_model=dict, status_code=status.HTTP_200_OK)
@inject
def get_all_users(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(5, ge=1, le=100, description="Number of users per page"),
    sort: str = Query("created_at", description="Field to sort by"),
    order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order (asc or desc)"),
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user)
):
    users = service.get_all_users(page=page, limit=limit, sort=sort, order=order)
    return {
        "message": "Users retrieved successfully",
        "result": users["result"],
        "pagination": {
            "current_page": page,
            "total_pages": users["total_pages"],
            "total_items": users["total_items"],
        },
    }

@router.get("/{user_id}", response_model=FindUserByOptionsResponse, status_code=status.HTTP_200_OK)
@inject
def get_user_by_id(
    user_id: uuid.UUID,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user),
):
    user = service.get_user_by_options(option="id", value=user_id)
    return {
        "message": "User retrieved successfully",
        "result": user,
    }

# UN-TESTED
# CURRENT ERROR: NEED TO DELETE THE PROFILE FIRST
@router.delete("/{user_id}", response_model=DeleteUserResponse, status_code=status.HTTP_200_OK)
@inject
def delete_user(
    user_id: uuid.UUID,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user)
):
    return service.delete_user(user_id)

@router.get("/me", response_model=FindUserByOptionsResponse, status_code=status.HTTP_200_OK)
@inject
def get_current_user(
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user)
):
    user = service.get_user_by_options("id", current_user["id"])

    return {
        "message": "User retrieved successfully",
        "result": user,
    }

@router.get("/me/profile", response_model=FindUserByOptionsResponse, status_code=status.HTTP_200_OK)
@inject
def get_current_user(
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user)
):
    user = service.get_user_by_options("id", current_user["id"])

    return {
        "message": "User retrieved successfully",
        "result": user,
    }

# UN-TESTED
# CURRENT ERROR: I THINK IT SHOULD BE PUT OR PATCH
@router.post("/me/profile", response_model=UpdateUserProfileResponse, status_code=status.HTTP_201_CREATED)
@inject
def attach_user_profile(
    profile_info,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user),
):
    user_id = current_user["id"]
    profile = service.attach_user_profile(user_id, profile_info)
    simplified_profile = profile.model_dump(exclude_none=True)

    return {
        "message": "Profile attached successfully",
        "result": simplified_profile,
    }

@router.patch("/me/profile", response_model=UpdateUserProfileResponse, status_code=status.HTTP_201_CREATED)
@inject
def attach_user_profile(
    profile_info,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_user),
):
    user_id = current_user["id"]
    profile = service.attach_user_profile(user_id, profile_info)
    simplified_profile = profile.model_dump(exclude_none=True)

    return {
        "message": "Profile attached successfully",
        "result": simplified_profile,
    }
    