from typing import Optional
from pydantic import BaseModel, Field

class ModelBaseInfo(BaseModel):
    id: str

class FindBase(BaseModel):
    ordering: Optional[str] = Field(default=None, description="Field to order by")
    page: Optional[int] = Field(default=1, ge=1, description="Page number")
    page_size: Optional[int] = Field(default=10, ge=1, le=100, description="Items per page")

class SearchOptions(FindBase):
    total_count: Optional[int]