class CalculatorServices:
    def __init__(self):
        pass

    def addition(self, num1, num2):
        return num1 + num2

    def subtraction(self, num1, num2):
        return num1 - num2

    def multiplication(self, num1, num2):
        return num1 * num2

    def division(self, num1, num2):
        if num2 == 0:
            raise ValueError("Division by zero is not allowed.")
        return num1 / num2
