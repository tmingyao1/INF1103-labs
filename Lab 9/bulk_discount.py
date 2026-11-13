from discount_strategy import DiscountStrategy

class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float):
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and amount cannot be negative.")
        self._threshold: float = threshold
        self._amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self._threshold:
            return total - self._amount
        return total