from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import Provide
from app.core.container import Container
from app.core.middleware import inject
from app.schema.auth_schema import RegisterSchema, LoginSchema, LoginResult
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
@inject
def sign_up(
    user: RegisterSchema,
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    result = service.sign_up(user)
    return result

@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResult)
@inject
def sign_in(
    credentials: LoginSchema,
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    return service.sign_in(credentials)

@router.post("/logout", status_code=status.HTTP_200_OK)
@inject
def sign_out(
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    return service.sign_out()