from uuid import UUID
from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, Field
from app.schema.base_schema import FindBase, ModelBaseInfo
from app.utils.schema import AllOptional

class BaseCompany(BaseModel):
    company_name: str
    year_of_assignment: int
    start_audit_period: datetime 
    end_audit_period: datetime    
    
    class Config:
        from_attributes: True

class Company(ModelBaseInfo, BaseCompany, metaclass=AllOptional): 
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes: True

class FindAllCompaniesResponse(BaseModel):
    message: str
    result: Optional[List[Company]]
    meta: Optional[FindBase]

class FindCompanyByOptionsRequest(BaseModel):
    option: str
    value: Optional[Union[str, UUID]]

class FindCompanyByOptionsResponse(BaseModel):
    message: str
    result: Optional[Union[List[Company], Company]]
    meta: Optional[FindBase]

class CreateCompanyRequest(BaseModel):
    company_name: str = Field(..., min_length=3, max_length=100)
    year_of_assignment: int
    start_audit_period: datetime 
    end_audit_period: datetime  

class CreateCompanyResponse(BaseModel):
    message: str
    result: Optional[Company]
    meta: Optional[FindBase]

class UpdateCompanyRequest(BaseModel):
    company_name: Optional[str] = Field(..., min_length=3, max_length=100)
    year_of_assignment: Optional[int]
    start_audit_period: Optional[datetime] 
    end_audit_period: Optional[datetime] 

class UpdateCompanyResponse(BaseModel):
    message: str
    result: Optional[Company]  
    meta: Optional[FindBase]

class DeleteCompanyResponse(BaseModel):
    message: str
    result: Optional[Company]  
    meta: Optional[FindBase]