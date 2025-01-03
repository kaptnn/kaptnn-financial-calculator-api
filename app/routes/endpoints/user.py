from fastapi import APIRouter, Depends,status
from dependency_injector.wiring import Provide
from app.core.container import Container
from app.core.middleware import inject
from app.core.dependencies import get_current_user
from app.schema.user_schema import FindUserByOptionsResult, AddPersonalInfoResult
from app.services.user_service import UserService, UserDict

router = APIRouter(prefix="/user", tags=["user"])

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

@router.post("/me/attach-profile", status_code=status.HTTP_201_CREATED, response_model=AddPersonalInfoResult, response_model_exclude_none=True)
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