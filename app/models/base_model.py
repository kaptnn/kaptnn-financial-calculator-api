from typing import Optional
from sqlmodel import Field, SQLModel

class BaseModel(SQLModel):
    id: Optional[int] = Field(primary_key=True, index=True, default=None)