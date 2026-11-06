from product import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int):
        # OrderLine refers to a Product but does not own it
        self._product: Product = product
        self._quantity: int = quantity

    def get_product(self) -> Product:
        return self._product

    def get_quantity(self) -> int:
        return self._quantity

    def calculate_subtotal(self) -> float:
        return self._product.get_price() * self._quantity

    def display_information(self) -> None:
        print(f"    {self._product.get_name()} x {self._quantity} "
              f"= ${self.calculate_subtotal():.2f}")