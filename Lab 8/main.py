from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory


def get_next_product_id(inventory: Inventory) -> str:
    highest = 0
    width = 3
    for p in inventory.get_all_products():
        pid = p.get_id()
        if pid.startswith("P") and pid[1:].isdigit():
            highest = max(highest, int(pid[1:]))
            width = len(pid[1:])
    return f"P{highest + 1:0{width}d}"


def read_positive_float(prompt: str) -> float:
    while True:
        value_input = input(prompt).strip()
        try:
            value = float(value_input)
            if value >= 0:
                return value
        except ValueError:
            pass
        print("Error: please enter a valid non-negative number.")


def choose_supplier(inventory: Inventory) -> Supplier:
    suppliers = inventory.get_all_suppliers()
    if suppliers:
        print("Existing suppliers:")
        for s in suppliers.values():
            s.display_information()

    supplier_id = input("Enter supplier ID (existing or new): ").strip().upper()
    if supplier_id in suppliers:
        return suppliers[supplier_id]

    print("New supplier.")
    name = input("Enter supplier name: ").strip()
    contact_email = input("Enter supplier email: ").strip()
    return Supplier(supplier_id, name, contact_email)


def add_product(inventory: Inventory) -> None:
    while True:
        print("Product type:")
        print("1. Physical")
        print("2. Digital")
        product_type = input("Enter type: ").strip()
        if product_type in ("1", "2"):
            break
        print("Error: please enter 1 or 2.")

    product_id = get_next_product_id(inventory)
    print(f"Product ID: {product_id}")

    while True:
        name = input("Enter product name: ").strip()
        if not name:
            print("Error: product name cannot be empty.")
        elif name.isdigit():
            print("Error: product name cannot be just numbers.")
        elif not any(ch.isalpha() for ch in name):
            print("Error: product name must contain at least one letter.")
        else:
            break

    while True:
        price_input = input("Enter price: ").strip()
        try:
            price = float(price_input)
            break
        except ValueError:
            print("Error: please enter a valid number for price.")

    while True:
        stock_input = input("Enter stock: ").strip()
        if stock_input.isdigit():
            stock = int(stock_input)
            break
        print("Error: please enter a valid non-negative integer.")

    supplier = choose_supplier(inventory)

    if product_type == "1":
        weight = read_positive_float("Enter weight (kg): ")
        product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
    else:
        download_size = read_positive_float("Enter download size (MB): ")
        product = DigitalProduct(product_id, name, price, stock, supplier, download_size)

    inventory.add_product(product)
    print("\nProduct added:")
    product.display_information()
    print()


def update_stock(inventory: Inventory) -> None:
    product_id = input("Enter product ID to update: ").strip()
    if inventory.find_product(product_id) is None:
        print("\nProduct not found.\n")
        return
    while True:
        stock_input = input("Enter new stock: ").strip()
        if stock_input.isdigit():
            inventory.update_stock(product_id, int(stock_input))
            print(f"\nUpdated product {product_id} to new stock: {stock_input}\n")
            return
        print("Error: please enter a valid non-negative integer.")


def search_product(inventory: Inventory) -> None:
    query = input("Enter product ID or name to search: ")
    results = inventory.search_product(query)
    if results:
        print("\nSearch Results:")
        for p in results:
            p.display_information()
        print()
    else:
        print("\nNo matching product found.\n")


def remove_product(inventory: Inventory) -> None:
    product_id = input("Enter product ID to remove: ").strip()
    product = inventory.remove_product(product_id)
    if product is None:
        print("\nProduct not found.\n")
    else:
        print(f"\nRemoved {product.get_name()} from the inventory.\n")


def print_menu() -> None:
    print("----- Inventory Menu -----")
    print("1. Display")
    print("2. Add")
    print("3. Update")
    print("4. Search")
    print("5. Remove")
    print("6. Save")
    print("7. Exit")


def main() -> None:
    inventory = Inventory()
    inventory.load()
    if not inventory.get_all_products():
        tech_supplier = Supplier("S001", "TechWorld Ltd", "sales@techworld.com")
        soft_supplier = Supplier("S002", "SoftHouse", "contact@softhouse.com")
        inventory.add_product(PhysicalProduct("P001", "Wireless Mouse", 25.50, 2, tech_supplier, 0.1))
        inventory.add_product(PhysicalProduct("P002", "Keyboard", 45.00, 1, tech_supplier, 0.8))
        inventory.add_product(DigitalProduct("P003", "Antivirus Software", 29.99, 3, soft_supplier, 850))

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            inventory.display_all_products()
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            remove_product(inventory)
        elif choice == "6":
            inventory.save()
        elif choice == "7":
            inventory.save()
            print(" ")
            print("Program terminated.")
            break
        else:
            print("\nInvalid choice. Please select 1-7.\n")


if __name__ == "__main__":
    main()