import unittest

from supplier import Supplier
from product_factory import ProductFactory
from order_line import OrderLine
from order import Order


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S001", "TechWorld Ltd", "sales@techworld.com")
        self.product = ProductFactory.create("physical", "P001", "Lamp", 25.0, 10,
                                             self.supplier, weight=1.2)

    def test_price_must_be_greater_than_zero(self):
        for bad_price in (0, -5):
            with self.assertRaises(ValueError):
                ProductFactory.create("physical", "P002", "Chair", bad_price, 3, self.supplier)

    def test_stock_cannot_be_negative_when_created(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D001", "Editor", 49.9, -1, self.supplier)

    def test_stock_cannot_be_updated_to_negative(self):
        with self.assertRaises(ValueError):
            self.product.update_stock(-3)
        self.assertEqual(self.product.get_stock(), 10)

    def test_both_product_types_keep_the_stock_rule(self):
        digital = ProductFactory.create("digital", "D001", "Editor", 49.9, 5, self.supplier)
        for product in (self.product, digital):
            with self.assertRaises(ValueError):
                product.update_stock(-1)

    def test_order_line_quantity_must_be_greater_than_zero(self):
        for bad_quantity in (0, -2):
            with self.assertRaises(ValueError):
                OrderLine(self.product, bad_quantity)

    def test_order_rejects_invalid_quantity(self):
        order = Order("O001")
        with self.assertRaises(ValueError):
            order.add_order_line(self.product, 0)
        self.assertEqual(order.get_order_lines(), [])


if __name__ == "__main__":
    unittest.main()