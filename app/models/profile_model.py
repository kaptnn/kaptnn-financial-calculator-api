import enum
from typing import Optional
from datetime import datetime
from sqlmodel import Field, Relationship, Enum, Column, DateTime, func
from app.models.base_model import BaseModel

class Membership(str, enum.Enum):
    default = "default"
    pro =  "pro"
    custom = "custom"
    
class Profile(BaseModel, table=True):
    __tablename__: str = "user_profile"

    user_id: int = Field(foreign_key="users.id")
    company: str = Field(nullable=False, default=None)
    membership_status: str = Field(sa_column=Column(Enum(Membership), nullable=False), default="default")
    
    created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), default=func.now()), default=None)
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()), default=None)
    
    user: Optional["User"] = Relationship(back_populates="profile")

from app.models.user_model import User
User.model_rebuild()