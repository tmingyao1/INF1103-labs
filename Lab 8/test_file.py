from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())

print("===== 2. ASSOCIATION: Supplier and Product =====")
supplier = Supplier("S001", "Music Gear Ltd", "orders@musicgear.com")
guitar = PhysicalProduct("P001", "Guitar", 299.99, 5, supplier, 4.2)
game = DigitalProduct("P002", "Video Game", 59.99, 100, supplier, 3000)

print("Supplier through each product:")
guitar.get_supplier().display_information()
game.get_supplier().display_information()

print("Guitar and its supplier are separate objects:", guitar is not guitar.get_supplier())
print("Both products share the same Supplier object:", guitar.get_supplier() is game.get_supplier())

del supplier
print("After 'del supplier', the products still know their supplier:")
guitar.get_supplier().display_information()

print("\n===== 3. AGGREGATION: Inventory and Product =====")
keyboard = PhysicalProduct("P003", "Keyboard", 45.00, 10, guitar.get_supplier(), 0.8)
print("Product created BEFORE any inventory exists:")
keyboard.display_information()

inventory_a = Inventory()
inventory_b = Inventory()

inventory_a.add_product(keyboard)
print("In Inventory A:", inventory_a.find_product("P003") is not None)

inventory_a.remove_product("P003")
print("In Inventory A after removal:", inventory_a.find_product("P003") is not None)
print("Product still works after removal:")
keyboard.display_information()

inventory_b.add_product(keyboard)
print("In Inventory B:", inventory_b.find_product("P003") is not None)
print("Same object moved to B:", inventory_b.find_product("P003") is keyboard)

print("\n===== 4. COMPOSITION: Order and OrderLine =====")
order1 = Order("O001")
order1.add_order_line(guitar, 2)
order1.add_order_line(game, 1)
order1.display_information()

order2 = Order("O002")
order2.add_order_line(guitar, 1)
order2.display_information()

line_in_order1 = order1.get_order_lines()[0]
line_in_order2 = order2.get_order_lines()[0]
print("Same OrderLine object in both orders:", line_in_order1 is line_in_order2)
print("Same Product object in both order lines:",
      line_in_order1.get_product() is line_in_order2.get_product())
print("OrderLine ids:", id(line_in_order1), id(line_in_order2))
print("Product ids:  ", id(line_in_order1.get_product()), id(line_in_order2.get_product()))

order1.remove_order_line("P002")
print("Order 1 after removing the Video Game line:")
order1.display_information()
print("Video Game product still exists:", game.get_name())

print("\n===== 6. LSP: show_product_details works with any Product =====")
show_product_details(guitar)
show_product_details(game)

print("\nBoth types used through normal Inventory operations:")
shop = Inventory()
shop.add_product(guitar)
shop.add_product(game)
for product_id in ("P001", "P002"):
    shop.find_product(product_id).update_stock(50)
shop.display_all_products()

print("===== 7. POLYMORPHISM: one loop, no isinstance =====")
for product in shop.get_all_products():
    product.display_information()
    print(product.get_fulfilment_info())