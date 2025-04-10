import uuid
import bcrypt
import base64
from typing import Any
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.core import security
from app.models.profile_model import Profile
from app.repositories.user_repo import UserRepository
from app.schema.auth_schema import RegisterSchema, LoginSchema
from app.core.exceptions import DuplicatedError, InternalServerError
from app.services.base_service import BaseService

class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def sign_up(self, user: RegisterSchema) -> dict:
        is_user_exist = self.user_repository.get_user_by_options("email", user.email)
        
        if is_user_exist is not None:
            raise DuplicatedError("User with this email already exists")

        encrypted_password = self.hash_password(user.password)
        new_user = self.user_repository.create_user(name=user.name, email=user.email, password=encrypted_password, company_id=uuid.UUID(user.company_id))

        if not new_user:
            raise InternalServerError("Failed to create user. Please try again later")

        print(f"    INFO : {new_user.id}, User Account Created Successfully!")

        new_user_profile = self.user_repository.create_user_profile(Profile(
            user_id=new_user.id if new_user.id is not None else 0
        ))

        if not new_user_profile:
            raise InternalServerError("Failed to create user profile. Please try again later")

        print(f"    INFO : {new_user.id} with {new_user_profile.id}, User Profile Created Successfully!")

        return {"message": "User successfully registered"}

    def sign_in(self, credentials: LoginSchema) -> Any:
        result = self.user_repository.get_user_by_options("email", credentials.email)

        if not result:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        user = result[0]

        print(f"    INFO : {user.id}, User with {credentials.email} Retrieved!")

        if not self.verify_password(credentials.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        print(f"    INFO : {user.id} Credentials Verified!")
        
        access_token = security.create_access_token(data={"sub": str(user.id)})
        refresh_token = security.create_refresh_token(data={"sub": str(user.id)})

        print(f"    INFO : {user.id}, Access Token & Refresh Token Created Successfully!")

        response = JSONResponse(
            content={
                "message": "User successfully logged in",
                "data": {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            })
        
        response.set_cookie(key="access_token", value=access_token, httponly=True, secure=False, samesite="none")
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=False, samesite="none")

        print(f"    INFO : {user.id}, Access Token & Refresh Token Already Set to the Site!")
        
        return response

    def sign_out(self):
        response = JSONResponse(content={"message": "Logged out"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        print(f"    INFO : Access Token & Refresh Token Deleted, Sign Out Success!")

        return response
    
    def create_new_access_token_service(self, refresh_token):
        return security.create_new_access_token(refresh_token)
    
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