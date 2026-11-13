from product import Product
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock: int, supplier: Supplier, weight: float = 0.0,
               download_size: float = 0.0) -> Product:
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock, supplier, weight)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock, supplier, download_size)
        else:
            raise ValueError(f"Unknown product type: {product_type}")