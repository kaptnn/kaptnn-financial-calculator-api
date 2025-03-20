import enum
import uuid
from typing import Optional
from sqlmodel import Field, Relationship, Enum, Column
from app.models.user_model import User
from app.models.base_model import BaseModel

class Role(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"
    client = "client"

class Membership(str, enum.Enum):
    basic = "basic"
    professional = "professional"
    enterprise = "enterprise"

class Profile(BaseModel, table=True):
    __tablename__ = "profiles"
    
    user_id: uuid.UUID = Field(foreign_key="users.id", unique=True)
    role: Role = Field(sa_column=Column(Enum(Role), nullable=False), default=Role.client)
    membership_status: Membership = Field(sa_column=Column(Enum(Membership), nullable=False), default=Membership.basic)
    is_verified: bool = Field(nullable=False, default=False)

    user: Optional["User"] = Relationship(back_populates="profile")
