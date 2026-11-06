from product import Product
from order_line import OrderLine


class Order:
    def __init__(self, order_id: str):
        self._order_id: str = order_id
        self._order_lines: list[OrderLine] = []

    def get_id(self) -> str:
        return self._order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self._order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for line in self._order_lines:
            if line.get_product().get_id() == product_id:
                self._order_lines.remove(line)
                return True
        return False

    def get_order_lines(self) -> list[OrderLine]:
        return list(self._order_lines)

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self._order_lines)

    def display_information(self) -> None:
        print(f"Order {self._order_id}:")
        for line in self._order_lines:
            line.display_information()
        print(f"    Total: ${self.calculate_total():.2f}")