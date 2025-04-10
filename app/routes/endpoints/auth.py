from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import Provide
from app.core.container import Container
from app.core.middleware import inject
from app.schema.auth_schema import UserRegisterRequest, UserRegisterResponse, UserLoginRequest, UserLoginResponse, UserLogoutResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRegisterResponse ,status_code=status.HTTP_201_CREATED)
@inject
def sign_up(
    user: UserRegisterRequest,
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    result = service.sign_up(user)
    return result

@router.post("/login", response_model=UserLoginResponse, status_code=status.HTTP_200_OK)
@inject
def sign_in(
    credentials: UserLoginRequest,
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    return service.sign_in(credentials)

@router.post("/logout", response_model=UserLogoutResponse, status_code=status.HTTP_200_OK)
@inject
def sign_out(
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    return service.sign_out()

@router.post("/token/refresh")
@inject
def create_new_access_token(
    refresh_token: str,
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    return service.create_new_access_token_service(refresh_token)