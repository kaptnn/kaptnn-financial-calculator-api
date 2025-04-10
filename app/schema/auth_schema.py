from pydantic import BaseModel

class UserRegisterRequest(BaseModel):
    name: str
    email: str
    company_id: str
    password: str
    
class UserRegisterResponse(BaseModel):
    message: str

class UserLoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str

class UserLoginResponse(BaseModel):
    message: str
    token: Token