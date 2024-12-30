class PresentValueServices:
    def __init__(self):
        pass

    def present_value(self, future_value, rate, period):
        rate_in_percentage = rate / 100
        return future_value / (1 + rate_in_percentage) ** period