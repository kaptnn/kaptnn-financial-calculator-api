from typing import Dict, Optional
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    company_id: UUID
    password: str = Field(..., min_length=8)
    
class UserRegisterResponse(BaseModel):
    message: str
    result: Optional[Dict]
    meta: Optional[Dict]

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class Token(BaseModel):
    token_type: str = Field(..., description="Token type, usually 'bearer'")
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")

class UserLoginResponse(BaseModel):
    message: str
    result: Token
    meta: Optional[Dict]

class UserLogoutResponse(BaseModel):
    message: str
    result:  Optional[Dict]
    meta: Optional[Dict]

class UserRefreshTokenRequest(BaseModel):
    refresh_token: str
    
class UserRefreshTokenResponse(BaseModel):
    message: str
    result: Token
    meta: Optional[Dict]