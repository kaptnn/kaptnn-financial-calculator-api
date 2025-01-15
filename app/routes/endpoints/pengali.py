from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import List
from app.services.calculator_service import CalculatorServices
from app.services.depreciation_calculator import PenyusutanCalculatorServices
from app.services.pengali_service import pengaliServices
from app.services.present_value_calculator import PresentValueServices
from app.services.goal_seeking_weighted_average import GoalSeekingWeightedAverage

router = APIRouter(prefix="/pengali", tags=["pengali"])

@router.get("/", status_code=status.HTTP_200_OK)
def pengali(
    num1: float = Query(..., description="First number"), 
    num2: float = Query(..., description="Second number"), 
    service: pengaliServices = Depends()
):
    result = service.pengali(num1=num1,num2=num2)
    return {"operation": "pengali", "num1": num1, "num2": num2, "result": result}