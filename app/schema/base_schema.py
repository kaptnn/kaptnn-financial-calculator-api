from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field

class ModelBaseInfo(BaseModel):
    id: UUID

    class Config:
        from_attributes = True

class FindBase(BaseModel):
    current_page: Optional[int] = Field(1, ge=1, description="Page number")
    total_pages: Optional[int]
    total_items: Optional[int]

class SearchOptions(FindBase):
    total_count: Optional[int] = Field(..., description="Total number of items matching the query")