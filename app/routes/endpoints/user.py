from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query,status
from dependency_injector.wiring import Provide
from app.core.container import Container
from app.core.middleware import inject
from app.core.dependencies import get_current_user
from app.models.profile_model import Profile
from app.schema.user_schema import FindUserByOptionsResult, AddPersonalInfoResult
from app.services.user_service import UserService, UserDict

router = APIRouter(prefix="/users", tags=["user"])

@router.get("/")
@inject
def get_all_users(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(5, ge=1, le=100, description="Number of users per page"),
    sort: str = Query("created_at", description="Field to sort by"),
    order: str = Query("asc", regex="^(asc|desc)$", description="Sort order (asc or desc)"),
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

@router.get("/user/{userId}")
@inject
def get_user_by_email(
    userId: str,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: UserDict = Depends(get_current_user),
):
    user = service.get_user_by_options(option="id", value=userId)
    return {
        "message": "User retrieved successfully",
        "data": user,
    }

@router.get("/me", response_model=FindUserByOptionsResult, response_model_exclude_none=True)
@inject
def get_user_by_options(
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: UserDict = Depends(get_current_user)
):
    user = service.get_user_by_options("id", current_user["id"])
    user["password"] = None

    return {
        "data": user,
        "message": "User retrieved successfully"
    }

@router.post("/me/profile", status_code=status.HTTP_201_CREATED, response_model=AddPersonalInfoResult, response_model_exclude_none=True)
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

@router.put("/verify", status_code=status.HTTP_200_OK)
@inject
def verify_user(
    user_id: int = Query(..., description="ID of the user to verify"),
    action: Literal["approve", "reject"] = Query(..., description="Action to perform: 'approve' or 'reject'"),
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: UserDict = Depends(get_current_user),
):
    user_profile: UserDict = service.get_user_by_options(option="id", value=user_id)

    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found.",
        )
    
    print(user_profile)
    if action == "approve":
        profile_info = Profile(
            id=user_profile["profile"]["id"],
            role="client", 
            is_verified=True,  
        )

        updated_profile = service.attach_user_profile(user_id, profile_info)

        return {
            "message": f"User with ID {user_id} has been approved and verified.",
            "profile": updated_profile,  
        }

    elif action == "reject":
        return {
            "message": f"User with ID {user_id} has been rejected and removed from the system.",
        }
