from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.schema.base_schema import ModelBaseInfo, FindBase
from app.models.profile_model import Membership
from app.utils.schema import AllOptional

class Profile(BaseModel):
    id: int
    user_id: int
    company: str
    membership: Membership
    created_at: datetime | None
    updated_at: datetime | None
    
class BaseUser(BaseModel):
    id: int
    email: str
    password: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    profile: Optional[Profile]

class User(ModelBaseInfo, BaseUser, metaclass=AllOptional): ...

class FindUser(FindBase, BaseUser, metaclass=AllOptional):
    ...

class FindUserResult(BaseModel):
    data: Optional[List[User]]
    message: str

class FindUserByOptions(BaseModel):
    option: str
    value: str | int


class FindUserByOptionsResult(BaseModel):
    data: Optional[User]
    message: str

class AddPersonalInfo(BaseModel):
    company: str
    membership: Membership


class PersonalInfo(Profile, AddPersonalInfo): ...

class AddPersonalInfoResult(BaseModel):
    data: PersonalInfo
    message: str