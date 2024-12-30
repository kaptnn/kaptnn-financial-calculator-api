from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import List
from app.services.calculator_service import CalculatorServices
from app.services.depreciation_calculator import PenyusutanCalculatorServices
from app.services.present_value_calculator import PresentValueServices
from app.services.goal_seeking_weighted_average import GoalSeekingWeightedAverage


router = APIRouter(prefix="/calculator", tags=["Calculator"])

@router.get("/addition", status_code=status.HTTP_200_OK)
def addition(
    num1: float = Query(..., description="First number"), 
    num2: float = Query(..., description="Second number"), 
    service: CalculatorServices = Depends()
):
    result = service.addition(num1, num2)
    return {"operation": "addition", "num1": num1, "num2": num2, "result": result}

@router.get("/subtraction", status_code=status.HTTP_200_OK)
def subtraction(
    num1: float = Query(..., description="First number"), 
    num2: float = Query(..., description="Second number"), 
    service: CalculatorServices = Depends()
):
    result = service.subtraction(num1, num2)
    return {"operation": "subtraction", "num1": num1, "num2": num2, "result": result}

@router.get("/multiplication", status_code=status.HTTP_200_OK)
def multiplication(
    num1: float = Query(..., description="First number"), 
    num2: float = Query(..., description="Second number"), 
    service: CalculatorServices = Depends()
):
    result = service.multiplication(num1, num2)
    return {"operation": "multiplication", "num1": num1, "num2": num2, "result": result}

@router.get("/division", status_code=status.HTTP_200_OK)
def division(
    num1: float = Query(..., description="First number"), 
    num2: float = Query(..., description="Second number"), 
    service: CalculatorServices = Depends()
):
    try:
        result = service.division(num1, num2)
        return {"operation": "division", "num1": num1, "num2": num2, "result": result}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/penyusutan", status_code=status.HTTP_200_OK)
def penyusutan(
    harga_perolehan: float = Query(..., description="Acquisition cost (must be > 0)"),
    estimasi_umur: float = Query(..., description="Estimated useful life in years (must be > 0)"),
    estimasi_nilai_sisa: float = Query(0, description="Residual value at the end of useful life (>= 0)"),
    metode: str = Query(..., description="Depreciation method ('straight_line' or 'double_declining')"),
    service: PenyusutanCalculatorServices = Depends()
):
    try:
        if metode not in ["straight_line", "double_declining"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Invalid method. Choose 'straight_line' or 'double_declining'."
            )
        
        if metode == "straight_line":
            biaya_per_bulan, biaya_per_tahun = service.straight_line(
                harga_perolehan, estimasi_umur, estimasi_nilai_sisa
            )
            return {
                "metode": metode,
                "biaya_per_bulan": biaya_per_bulan,
                "biaya_per_tahun": biaya_per_tahun,
            }
        else:
            biaya_per_bulan_list, biaya_per_tahun_list = service.double_declining(
                harga_perolehan, estimasi_umur, estimasi_nilai_sisa
            )
            return {
                "metode": metode,
                "biaya_per_bulan": biaya_per_bulan_list,
                "biaya_per_tahun": biaya_per_tahun_list,
            }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/present-value", status_code=status.HTTP_200_OK)
def present_value(
    future_value: float = Query(..., description="Future Value (must be > 0)"),
    rate: float = Query(..., description="Rate in %"),
    period: float = Query(0, description="Period times"),
    service: PresentValueServices = Depends()
):
    try:      
        present_value = service.present_value(future_value, rate, period)
        return {
            "present_value": present_value,
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/weighted-average", status_code=status.HTTP_200_OK)
def weighted_average(
    n_total: float = Query(1, description="Total row of loss rate and weight"), 
    loss_rate_array: List[float] = Query(..., description="Lost rate value in %"),
    weight_array: List[float] = Query(..., description="Weight value in %"),
    service: GoalSeekingWeightedAverage = Depends()
):
    try:      
        if len(loss_rate_array) != n_total and len(weight_array) != n_total:
            raise ValueError("The length of loss_rate_array and weight_array must match n_total.")

        normal_average = service.normal_average(loss_rate_array)
        weighted_average = service.weighted_average(loss_rate_array, weight_array)

        weight_difference = service.weight_difference(weight_array)
    
        return {
            "normal_average": normal_average,
            "weighted_average": weighted_average,
            "weight_difference": weight_difference,
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
