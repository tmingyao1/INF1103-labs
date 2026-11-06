from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float):
        super().__init__(product_id, name, price, stock, supplier)
        self._download_size: float = download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"    Type: Digital, Download size: {self._download_size} MB")

    def get_fulfilment_info(self) -> str:
        return f"{self._name} is delivered digitally via a download link."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self._download_size
        return data