from uuid import UUID
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.schema.base_schema import FindBase, ModelBaseInfo
from app.models.profile_model import Membership, Role
from app.utils.schema import AllOptional

class Profile(ModelBaseInfo, metaclass=AllOptional):
    user_id: UUID
    role: Role
    membership_status: Membership
    is_verified: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes: True
    
class BaseUser(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    company_id: Optional[UUID]
    password: Optional[str]
    
    class Config:
        from_attributes: True

class User(ModelBaseInfo, BaseUser, metaclass=AllOptional):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    profile: Optional[Profile]

    class Config:
        from_attributes: True

class FindAllUsersResponse(BaseModel):
    message: str
    result: Optional[List[User]]
    meta: Optional[FindBase]

class FindUserByOptionsRequest(BaseModel):
    option: str
    value: Optional[Union[str, UUID]]

class FindUserByOptionsResponse(BaseModel):
    message: str
    result: Optional[User]
    meta: Optional[FindBase]

class DeleteUserResponse(BaseModel):
    message: str
    result: Optional[User]
    meta: Optional[FindBase]

class FindUserProfileResponse(BaseModel):
    message: str
    result: Optional[Profile]
    meta: Optional[FindBase]

class CreateUserProfileRequest():
    role: Role
    membership_status: Membership
    is_verified: bool = Field(False, description="Whether the profile is verified")

class CreateUserProfileResponse():
    message: str
    result: Optional[Profile]
    meta: Optional[FindBase]

class UpdateUserProfileRequest(BaseModel):
    role: Optional[Role]
    membership_status: Optional[Membership]
    is_verified: Optional[bool]

class UpdateUserProfileResponse(BaseModel):
    message: str
    result: Optional[Profile]
    meta: Optional[FindBase]