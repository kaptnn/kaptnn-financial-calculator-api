import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.schema.base_schema import ModelBaseInfo
from app.utils.schema import AllOptional

class BaseCompany(BaseModel):
    company_name: str
    year_of_assignment: int
    start_audit_period: datetime 
    end_audit_period: datetime    
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class Company(ModelBaseInfo, BaseCompany, metaclass=AllOptional): ...

class FindAllCompaniesResponse(BaseModel):
    message: str
    result: Optional[List[Company]]

class FindCompanyByOptionsRequest(BaseModel):
    option: str
    value: str | uuid.UUID

class FindCompanyByOptionsResponse(BaseModel):
    message: str
    result: Optional[Company]

class CreateCompanyRequest(BaseModel):
    company_name: str
    year_of_assignment: int
    start_audit_period: datetime 
    end_audit_period: datetime    

class CreateCompanyResponse(BaseModel):
    message: str
    result: Company

class UpdateCompanyRequest(BaseModel):
    company_name: Optional[str]
    year_of_assignment: Optional[int]
    start_audit_period: Optional[datetime] 
    end_audit_period: Optional[datetime]    

class UpdateCompanyResponse(BaseModel):
    message: str
    result: Optional[Company]  

class DeleteCompanyResponse(BaseModel):
    message: str