from product import Product
from supplier import Supplier
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float):
        super().__init__(product_id, name, price, stock, supplier)
        self._weight: float = weight

    def display_information(self) -> None:
        super().display_information()
        print(f"    Type: Physical, Weight: {self._weight} kg, "
              f"Shipping cost: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self) -> str:
        return f"{self._name} requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return 3.99 + self._weight * 1.50

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self._weight
        return data