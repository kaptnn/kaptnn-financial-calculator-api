from typing import Optional
from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from dependency_injector.wiring import Provide
from app.core.container import Container
from app.core.dependencies import get_current_user
from app.core.middleware import inject
from app.schema.auth_schema import UserRefreshTokenRequest, UserRefreshTokenResponse, UserRegisterRequest, UserRegisterResponse, UserLoginRequest, UserLoginResponse, UserLogoutResponse
from app.schema.user_schema import User
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", 
    response_model=UserRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude={"result": {"__all__": {"password"}}}, 
    response_model_exclude_none=True)
@inject
def sign_up(
    user: UserRegisterRequest,
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    return service.sign_up(user)

@router.post("/login", 
    response_model=UserLoginResponse, 
    status_code=status.HTTP_200_OK,
    response_model_exclude={"result": {"__all__": {"password"}}}, 
    response_model_exclude_none=True)
@inject
def sign_in(
    credentials: UserLoginRequest,
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    return service.sign_in(credentials)

@router.post("/logout", 
    response_model=UserLogoutResponse, 
    status_code=status.HTTP_200_OK,
    response_model_exclude={"result": {"__all__": {"password"}}}, 
    response_model_exclude_none=True)
@inject
def sign_out(
    service: AuthService = Depends(Provide[Container.auth_service]),
    current_user: User = Depends(get_current_user)
):
    return service.sign_out()

@router.post("/token/refresh", 
    response_model=UserRefreshTokenResponse,
    status_code=status.HTTP_200_OK,
    response_model_exclude={"result": {"__all__": {"password"}}}, 
    response_model_exclude_none=True)
@inject
def create_new_access_token(
    credentials: UserRefreshTokenRequest = Depends(),
    refresh_token_cookie: Optional[str] = Cookie(None),
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    token = credentials.refresh_token or refresh_token_cookie
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing refresh token",
        )
    return service.create_new_access_token_service(token)

@router.get('/me')
@inject
def authenticated_user():
    pass

@router.get('/verify-email')
@inject
def authenticated_use():
    pass

@router.post('/verify-email/resend')
@inject
def authenticated_use():
    pass

@router.post('/password/forgot')
@inject
def authenticated_use():
    pass


@router.post('/password/reset')
@inject
def authenticated_use():
    pass

@router.post('/password/change')
@inject
def authenticated_use():
    pass

@router.get('/sessions')
@inject
def authenticated_use():
    pass

@router.delete('/sessions')
@inject
def authenticated_use():
    pass