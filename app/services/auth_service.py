from uuid import UUID
import bcrypt
import base64
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.core import security
from app.repositories.user_repo import UserRepository
from app.schema.auth_schema import Token, UserLogoutResponse, UserRefreshTokenRequest, UserRefreshTokenResponse, UserRegisterRequest, UserLoginRequest, UserRegisterResponse, UserLoginResponse
from app.core.exceptions import DuplicatedError, InternalServerError
from app.services.base_service import BaseService

class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def sign_up(self, user: UserRegisterRequest) -> UserRegisterResponse:
        is_user_exist = self.user_repository.get_user_by_options("email", user.email)
        
        if is_user_exist and is_user_exist.result:
            raise DuplicatedError("User with this email already exists")

        encrypted_password = self.hash_password(user.password)
        new_user = self.user_repository.create_user(name=user.name, email=user.email, password=encrypted_password, company_id=user.company_id)

        if not new_user:
            raise InternalServerError("Failed to create user. Please try again later")

        user_id = new_user.id

        new_user_profile = self.user_repository.create_user_profile(user_id)
        
        if not new_user_profile:
            self.user_repository.delete_user(user_id)
            raise InternalServerError("Failed to create user profile. Please try again later")
        
        return UserRegisterResponse(
            message="User successfully registered",
            result=None,
            meta=None
        )

    def sign_in(self, credentials: UserLoginRequest) -> UserLoginResponse:
        user = self.user_repository.get_user_by_options("email", credentials.email)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if not self.verify_password(credentials.password, user.result.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        access_token = security.create_access_token(data={"sub": str(user.result.id)})
        refresh_token = security.create_refresh_token(data={"sub": str(user.result.id)})

        response = JSONResponse(
            content={
                'message': "User successfully logged in",
                'result': {
                    'token_type': 'Bearer',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                },
                'meta': None
            }
        )
        
        response.set_cookie(key="access_token", value=access_token, httponly=True, secure=False, samesite="none")
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=False, samesite="none")
        
        return response

    def sign_out(self) -> UserLogoutResponse:
        response = JSONResponse(content={"message": "Logged out"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response
    
    def create_new_access_token_service(self, refresh_token: str) -> UserRefreshTokenResponse:
        token = security.create_new_access_token(refresh_token)
        return UserRefreshTokenResponse(
            message="Renew token is generated",
            result=token,
            meta=None
        )
    
    def forgot_password(self):
        pass

    def email_verification(self):
        pass

    def renew_session(self):
        pass

    def revoke_all_sessions(self):
        pass

    def revoke_session(self):
        pass

    def sign_with_social_account(self):
        pass

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return base64.b64encode(hashed).decode("utf-8")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        hashed_bytes = base64.b64decode(hashed_password)
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_bytes)