from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import List
from app.services.goal_seeking_weighted_average import GoalSeekingWeightedAverage

router = APIRouter(prefix="/goal-seeking", tags=["Goal Seeking"])

@router.get("/weighted-average", status_code=status.HTTP_200_OK)
def goal_seeking(
    n_total: int = Query(1, description="Total row of loss rate and weight"),
    goal: float = Query(..., description="Target weighted average"),
    weight_array: List[float] = Query(..., description="Weight value in %"),
    service: GoalSeekingWeightedAverage = Depends()
):
    try:
        if n_total != len(weight_array):
            raise ValueError("The length of weight_array must match n_total.")

        weight_diffs = service.weight_difference(weight_array)

        def weighted_avg_for_goal(initial_loss_rate, weights, weight_diffs):
            loss_rates = service.calculate_loss_rates(initial_loss_rate, weight_diffs)
            return service.weighted_average(loss_rates, weights)

        initial_loss_rate = service.goal_seek(
            func=weighted_avg_for_goal,
            goal=goal,
            args=(weight_array, weight_diffs)
        )

        loss_rate_array = service.calculate_loss_rates(initial_loss_rate, weight_diffs)

        normal_average = service.normal_average(loss_rate_array)
        weighted_average = service.weighted_average(loss_rate_array, weight_array)
        
        if any(rate >= 100 for rate in loss_rate_array[:-1]):
            raise ValueError("Computed loss rates exceed 100 before the last period.")

        return {
            "initial_loss_rate": initial_loss_rate,
            "loss_rate_array": loss_rate_array,
            "normal_average": normal_average,
            "weighted_average": weighted_average,
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))