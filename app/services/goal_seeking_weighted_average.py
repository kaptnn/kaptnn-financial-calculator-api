from scipy.optimize import root_scalar
from openpyxl import Workbook
from typing import List

class GoalSeekingWeightedAverage:
    def __init__(self):
        pass

    def normal_average(self, values):
        if not values:
            raise ValueError("The input list cannot be empty.")
        return sum(values) / len(values)
    
    def weighted_average(self, values, weights):
        if len(values) != len(weights):
            raise ValueError("Values and weights must have the same length.")
        if not values or not weights:
            raise ValueError("Values and weights cannot be empty.")
        return sum(v * w for v, w in zip(values, weights)) / sum(weights)

    def weight_difference(self, weights):
        if not weights:
            raise ValueError("Weights array cannot be empty.")

        if weights[0] == 0:
            raise ValueError("The weight of the first row cannot be zero.")

        weight_differences = [(weights[i] / weights[0]) - 1 if i > 0 else 0 for i in range(len(weights))]
        
        return weight_differences
    
    def calculate_loss_rates(self, initial_loss_rate: float, weight_diffs: List[float]) -> List[float]:
        loss_rates = [initial_loss_rate]
        for i, diff in enumerate(weight_diffs[1:], start=1):
            next_loss_rate = loss_rates[0] * (1 + diff)
            if i == len(weight_diffs) - 1:
                next_loss_rate = 100  
            loss_rates.append(min(next_loss_rate, 100)) 
        return loss_rates

    def goal_seek(self, func, goal, args):
        def wrapper(x):
            return func(x, *args) - goal
        result = root_scalar(wrapper, bracket=[0, 100], method='bisect')
        if not result.converged:
            raise ValueError("Goal seeking failed to converge.")
        return result.root
    
    def export_to_excel(self, values: List[float], weights: List[float], goal: float, file_name: str = "Results.xlsx"):
        wb = Workbook()
        ws = wb.active
        ws.title = "Results"

        ws.append(["Values", "Weights", "Weighted Average", "Goal Seek Result"])

        wa = self.weighted_average(values, weights)
        gs = self.goal_seek(lambda x, v, w: self.weighted_average(v, [x] + w[1:]), goal, (values, weights))

        ws.append([str(values), str(weights), wa, gs])

        file_path = f"/tmp/{file_name}" 
        wb.save(file_path)
        return file_path