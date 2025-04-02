from datetime import datetime
from pydantic import BaseModel

from app.models.company_model import Company

class CreateCompanySchema(BaseModel):
    company_name: str
    year_of_assignment: int
    start_audit_period: datetime 
    end_audit_period: datetime    

class CreateCompanyResult(BaseModel):
    message: str
    data: Company