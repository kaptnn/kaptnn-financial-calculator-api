import uuid
from fastapi import APIRouter, Depends, Query, status
from dependency_injector.wiring import Provide
from app.core.container import Container
from app.core.middleware import inject
from app.core.dependencies import get_current_user
from app.schema.user_schema import DeleteUserResponse, FindUserByOptionsResponse, UpdateUserProfileResponse
from app.services.user_service import UserService, UserDict

router = APIRouter(prefix="/users", tags=["user"])

@router.get("/", response_model=dict, status_code=status.HTTP_200_OK)
@inject
def get_all_users(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(5, ge=1, le=100, description="Number of users per page"),
    sort: str = Query("created_at", description="Field to sort by"),
    order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order (asc or desc)"),
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: UserDict = Depends(get_current_user)
):
    users = service.get_users(page=page, limit=limit, sort=sort, order=order)
    return {
        "message": "Users retrieved successfully",
        "data": users["results"],
        "pagination": {
            "current_page": page,
            "total_pages": users["total_pages"],
            "total_items": users["total_items"],
        },
    }

@router.get("/user/id/{id}", response_model=FindUserByOptionsResponse, status_code=status.HTTP_200_OK)
@inject
def get_user_by_id(
    id: str,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: UserDict = Depends(get_current_user),
):
    user = service.get_user_by_options(option="id", value=id)
    return {
        "message": "User retrieved successfully",
        "data": user,
    }

@router.get("/user/email/{email}", response_model=FindUserByOptionsResponse, status_code=status.HTTP_200_OK)
@inject
def get_user_by_email(
    email: str,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: UserDict = Depends(get_current_user),
):
    user = service.get_user_by_options(option="email", value=email)
    return {
        "message": "User retrieved successfully",
        "data": user,
    }

@router.get("/user/company/{company_id}", response_model=FindUserByOptionsResponse, status_code=status.HTTP_200_OK)
@inject
def get_user_by_company(
    company_id: uuid.UUID,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: UserDict = Depends(get_current_user),
):
    user = service.get_user_by_options(option="company_id", value=company_id)
    return {
        "message": "User retrieved successfully",
        "data": user,
    }

@router.get("/me", response_model=FindUserByOptionsResponse, status_code=status.HTTP_200_OK)
@inject
def get_current_user(
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: UserDict = Depends(get_current_user)
):
    user = service.get_user_by_options("id", current_user["id"])
    user["password"] = None

    return {
        "data": user,
        "message": "User retrieved successfully"
    }

@router.post("/me/profile", response_model=UpdateUserProfileResponse, status_code=status.HTTP_201_CREATED)
@inject
def attach_user_profile(
    profile_info,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: UserDict = Depends(get_current_user),
):
    user_id = current_user["id"]
    profile = service.attach_user_profile(user_id, profile_info)
    simplified_profile = profile.model_dump(exclude_none=True)

    return {
        "data": simplified_profile,
        "message": "Profile attached successfully"
    }

@router.delete("/user/id/{id}", response_model=DeleteUserResponse, status_code=status.HTTP_200_OK)
@inject
def delete_user():
    pass