import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from supplier import Supplier
from inventory import Inventory
from product_loader import load_products

CSV_TEXT = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


class TestLoadProducts(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S001", "TechWorld Ltd", "sales@techworld.com")
        self.inventory = Inventory()

    def run_loader(self, path: str) -> str:
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(path, self.inventory, self.supplier)
        return output.getvalue()

    def test_valid_rows_load_and_bad_rows_are_skipped(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "products.csv")
            with open(path, "w", newline="") as file:
                file.write(CSV_TEXT)
            output = self.run_loader(path)

        ids = [p.get_id() for p in self.inventory.get_all_products()]
        self.assertEqual(ids, ["P001", "D001", "P003"])
        self.assertIn("Unknown product type: service", output)
        self.assertIn("Office Chair", output)
        self.assertIn("3 products loaded.", output)
        self.assertTrue(output.strip().endswith("Load attempt finished."))

    def test_missing_file_is_handled_gracefully(self):
        output = self.run_loader("does_not_exist.csv")
        self.assertIn("Products file not found: does_not_exist.csv", output)
        self.assertIn("Load attempt finished.", output)
        self.assertNotIn("products loaded", output)
        self.assertEqual(self.inventory.get_all_products(), [])


if __name__ == "__main__":
    unittest.main()