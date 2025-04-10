from typing import List, Optional
import uuid
from pydantic import BaseModel
from datetime import datetime
from app.schema.base_schema import ModelBaseInfo
from app.models.profile_model import Membership, Role
from app.utils.schema import AllOptional

class Profile(ModelBaseInfo):
    user_id: str
    role: Role
    membership: Membership
    is_verified: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
class BaseUser(BaseModel):
    name: str
    email: str
    password: Optional[str]
    company_id: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    profile: Optional[Profile]

class User(ModelBaseInfo, BaseUser, metaclass=AllOptional): ...

class FindAllUsersResponse(BaseModel):
    message: str
    result: Optional[List[User]]

class FindUserByOptionsRequest(BaseModel):
    option: str
    value: str | int | uuid.UUID

class FindUserByOptionsResponse(BaseModel):
    message: str
    result: Optional[User]

class UpdateUserProfileRequest(BaseModel):
    role: Optional[Role]
    membership: Optional[Membership]
    is_verified: Optional[bool]

class UpdateUserProfileResponse(BaseModel):
    message: str
    result: Optional[User]