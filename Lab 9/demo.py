"""Runs each 'Predict first' scenario from Lab 9 so you can compare with your predictions."""
from supplier import Supplier
from inventory import Inventory
from order import Order
from product_factory import ProductFactory
from bulk_discount import BulkDiscount
from percentage_discount import PercentageDiscount
from student_discount import StudentDiscount
from product_loader import load_products

supplier = Supplier("S001", "TechWorld Ltd", "sales@techworld.com")

print("===== 2.3 Strategy: order lines adding up to 250 =====")
chair = ProductFactory.create("physical", "P001", "Chair", 100.00, 10, supplier, weight=5.0)
ebook = ProductFactory.create("digital", "D001", "E-Book", 50.00, 10, supplier, download_size=5)
order = Order("O001", BulkDiscount(200, 20))
order.add_order_line(chair, 2)
order.add_order_line(ebook, 1)
order.display_information()
order.set_discount(PercentageDiscount(10))
print(f"After set_discount(PercentageDiscount(10)): ${order.calculate_total():.2f}")

print("\n===== 2.4 New strategy without changing Order =====")
order.set_discount(StudentDiscount())
print(f"With StudentDiscount (5% off): ${order.calculate_total():.2f}")

print("\n===== 2.4 Two orders sharing one strategy object =====")
shared = PercentageDiscount(10)
order_a = Order("O002", shared)
order_b = Order("O003", shared)
order_a.add_order_line(chair, 1)
order_b.add_order_line(ebook, 2)
print(f"Order A total: ${order_a.calculate_total():.2f}, Order B total: ${order_b.calculate_total():.2f}")

print("\n===== 3.2 Factory with an unknown type (caught here) =====")
try:
    ProductFactory.create("service", "S001", "Installation", 30.00, 5, supplier)
except ValueError as error:
    print(f"ValueError: {error}")

print("\n===== 4 Validation =====")
for description, action in [
    ("Price of 0", lambda: ProductFactory.create("physical", "P9", "Free Pen", 0, 1, supplier)),
    ("Stock of -1", lambda: ProductFactory.create("digital", "D9", "App", 9.99, -1, supplier)),
    ("Order quantity of 0", lambda: order.add_order_line(chair, 0)),
    ("Digital update_stock(-5)", lambda: ebook.update_stock(-5)),
]:
    try:
        action()
        print(f"{description}: accepted")
    except ValueError as error:
        print(f"{description}: rejected - {error}")

print("\n===== 5.2 Loading products.csv =====")
inventory = Inventory()
load_products("products.csv", inventory, supplier)
inventory.display_all_products()

print("===== 5.2 Loading a file that does not exist =====")
load_products("missing_products.csv", Inventory(), supplier)
#ProductFactory.create("service", "S001", "Installation", 30.00, 5, supplier)