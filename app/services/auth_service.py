import bcrypt
import base64
from typing import Any
from fastapi import BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from app.core import security
from app.repositories.user_repo import UserRepository
from app.schema.auth_schema import RegisterSchema, LoginSchema
from app.models.profile_model import Profile
from app.core.exceptions import DuplicatedError, InternalServerError
from app.services.base_service import BaseService
from app.core.config import configs

conf = ConnectionConfig(
    MAIL_USERNAME=configs.MAIL_USERNAME,
    MAIL_PASSWORD=configs.MAIL_PASSWORD,
    MAIL_FROM=configs.MAIL_FROM,
    MAIL_PORT=configs.MAIL_PORT,
    MAIL_SERVER=configs.MAIL_SERVER,
    MAIL_STARTTLS=configs.MAIL_STARTTLS,
    MAIL_SSL_TLS=configs.MAIL_SSL_TLS,
    USE_CREDENTIALS=configs.USE_CREDENTIALS,
    VALIDATE_CERTS=configs.VALIDATE_CERTS,
)

class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def sign_up(self, background_tasks: BackgroundTasks, user: RegisterSchema) -> dict:
        is_user_exist = self.user_repository.get_user_by_options("email", user.email)
        
        if is_user_exist is not None:
            raise DuplicatedError("User with this email already exists")

        encrypted_password = self.hash_password(user.password)
        new_user = self.user_repository.create_user(name=user.name, email=user.email, password=encrypted_password)

        if not new_user:
            raise InternalServerError("Failed to create user. Please try again later")

        user_profile = self.user_repository.create_user_profile(company=user.company, user_id=new_user.id)

        # destination_email = "elsamrafisptr@gmail.com"
        # self.send_verification_email(background_tasks, destination_email, new_user, user_profile)
        
        return {"message": "User successfully registered"}

    def sign_in(self, credentials: LoginSchema) -> Any:
        result = self.user_repository.get_user_by_options("email", credentials.email)

        if not result:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        user = result[0]
        # if not user.is_verified:
        #     raise HTTPException(status_code=403, detail="Account not verified. Contact the administrator.")

        if not self.verify_password(credentials.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        access_token = security.create_access_token(data={"sub": str(user.id), "membership_status": result[1].membership_status.value})
        refresh_token = security.create_refresh_token(data={"sub": str(user.id)})

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
        
        return response

    def sign_out(self):
        response = JSONResponse(content={"message": "Logged out"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response

    def send_verification_email(self, background_tasks: BackgroundTasks, email: str, user: Any, user_profile: Any) -> None:
        verification_link = f"http://127.0.0.1:8000/verify?user_id={user.id}"
        email_body = f"""
        A new user has registered:
        Name: {user.name}
        Email: {user.email}
        Company: {user_profile.company}

        Please review their registration and assign a role:
        Approve: {verification_link}&action=approve
        Reject: {verification_link}&action=reject
        """

        message = MessageSchema(
            subject="New User Registration - Action Required",
            recipients=[email],
            body=email_body,
            subtype="plain"
        )

        fm = FastMail(conf)
        try:
            background_tasks.add_task(fm.send_message, message)
            print(f"Verification email sent to {email}")
            print(f"Sending email to {email}:\n{email_body}")
        except Exception as e:
            print(f"Failed to send email: {e}")
            raise InternalServerError("Failed to send verification email")

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return base64.b64encode(hashed).decode("utf-8")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        hashed_bytes = base64.b64decode(hashed_password)
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_bytes)