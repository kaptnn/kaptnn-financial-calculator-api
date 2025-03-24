from pydantic import BaseModel

from app.models.company_model import Company

class CreateCompanySchema(BaseModel):
    company_name: str
 
class CreateCompanyResult(BaseModel):
    message: str
    data: Company