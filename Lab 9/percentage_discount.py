from discount_strategy import DiscountStrategy

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self._percentage: float = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self._percentage / 100)