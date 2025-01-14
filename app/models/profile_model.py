import enum
from typing import Optional
from datetime import datetime
from sqlmodel import Field, Relationship, Enum, Column, DateTime, func
from app.models.base_model import BaseModel

class Role(str, enum.Enum):
    guest = "guest"
    client = "client"
    admin = "admin"

class Membership(str, enum.Enum):
    default = "default"
    pro = "pro"
    custom = "custom"

class Profile(BaseModel, table=True):
    __tablename__ = "user_profile" 
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    company: str = Field(nullable=False)
    role: Role = Field(sa_column=Column(Enum(Role), nullable=False), default=Role.guest)
    membership_status: Membership = Field(sa_column=Column(Enum(Membership), nullable=False), default=Membership.default)
    is_verified: bool = Field(nullable=False, default=False)

    created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))

    user: Optional["User"] = Relationship(back_populates="profile")

from app.models.user_model import User
User.model_rebuild()
