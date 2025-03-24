import uuid
from pydantic import BaseModel

class RegisterSchema(BaseModel):
    name: str
    email: str
    company_id: str
    password: str
    
class RegisterResult(BaseModel):
    message: str

class LoginSchema(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str

class LoginResult(BaseModel):
    message: str
    token: Token