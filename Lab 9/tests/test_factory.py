import unittest

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory


class TestProductFactory(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S001", "TechWorld Ltd", "sales@techworld.com")

    def test_creates_physical_product(self):
        product = ProductFactory.create("physical", "P001", "Lamp", 25.0, 10,
                                        self.supplier, weight=1.2)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)

    def test_creates_digital_product(self):
        product = ProductFactory.create("digital", "D001", "Editor", 49.9, 100,
                                        self.supplier, download_size=500)
        self.assertIsInstance(product, DigitalProduct)
        self.assertIsInstance(product, Product)

    def test_unknown_type_raises_value_error_with_clear_message(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Installation", 30.0, 5, self.supplier)
        self.assertEqual(str(context.exception), "Unknown product type: service")


if __name__ == "__main__":
    unittest.main()