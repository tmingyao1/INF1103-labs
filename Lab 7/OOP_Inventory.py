import json
import os
from abc import ABC, abstractmethod

INVENTORY_FILE = "inventory.json"

class Product(ABC):
    def __init__(self, product_id, name, price, stock):
        # Protected attributes (single underscore) so subclasses can use them
        self._product_id = product_id
        self._name = name
        self._price = price
        self._stock = stock

    def get_id(self):
        return self._product_id

    def get_name(self):
        return self._name

    def update_stock(self, new_stock):
        self._stock = new_stock

    def to_dict(self):
        return {
            "id": self._product_id,
            "name": self._name,
            "price": self._price,
            "stock": self._stock
        }

    def display_information(self):
        print(f"ID: {self._product_id}, Name: {self._name}, "
              f"Price: ${self._price:.2f}, Stock: {self._stock}")

    @abstractmethod
    def get_fulfilment_info(self):
        pass


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self._weight = weight

    def display_information(self):
        super().display_information()
        print(f"    Type: Physical, Weight: {self._weight} kg")

    def get_fulfilment_info(self):
        return f"{self._name} requires physical shipping."

    def calculate_shipping_cost(self):
        return 3.99 + self._weight * 1.50

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self._weight
        return data


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self._download_size = download_size

    def display_information(self):
        super().display_information()
        print(f"    Type: Digital, Download size: {self._download_size} MB")

    def get_fulfilment_info(self):
        return f"{self._name} is delivered digitally via a download link."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self._download_size
        return data


def create_product_from_dict(d):

    stock = d.get("stock", d.get("quantity", 0))
    if d.get("type") == "digital":
        return DigitalProduct(d.get("id"), d.get("name"), d.get("price"),
                              stock, d.get("download_size", 0.0))
    return PhysicalProduct(d.get("id"), d.get("name"), d.get("price"),
                           stock, d.get("weight", 0.0))


class Inventory:
    def __init__(self):
        self._products = []

    def add_product(self, product):
        self._products.append(product)

    def find_by_id(self, product_id):
        for p in self._products:
            if p.get_id() == product_id:
                return p
        return None

    def update_stock(self, product_id, new_stock):
        product = self.find_by_id(product_id)
        if product is None:
            return False
        product.update_stock(new_stock)
        return True

    def search_product(self, query):
        query = query.strip().lower()
        return [p for p in self._products
                if query == p.get_id().lower() or query in p.get_name().lower()]

    def get_all_products(self):
        return self._products

    def save(self):
        data = [p.to_dict() for p in self._products]
        with open(INVENTORY_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print("Saving inventory before exit...")
        print("Inventory saved to inventory.json")

    def load(self):
        self._products = []
        if not os.path.exists(INVENTORY_FILE):
            return
        with open(INVENTORY_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return
        for d in data:
            self._products.append(create_product_from_dict(d))


def get_next_product_id(inventory):
    highest = 0
    width = 3
    for p in inventory.get_all_products():
        pid = p.get_id()
        if pid.startswith("P") and pid[1:].isdigit():
            highest = max(highest, int(pid[1:]))
            width = len(pid[1:])
    return f"P{highest + 1:0{width}d}"


def read_positive_float(prompt):
    while True:
        value_input = input(prompt).strip()
        try:
            value = float(value_input)
            if value >= 0:
                return value
        except ValueError:
            pass
        print("Error: please enter a valid non-negative number.")


def add_product(inventory):
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

    if product_type == "1":
        weight = read_positive_float("Enter weight (kg): ")
        product = PhysicalProduct(product_id, name, price, stock, weight)
    else:
        download_size = read_positive_float("Enter download size (MB): ")
        product = DigitalProduct(product_id, name, price, stock, download_size)

    inventory.add_product(product)
    print("\nProduct added:")
    product.display_information()
    print()


def update_stock(inventory):
    product_id = input("Enter product ID to update: ").strip()
    if inventory.find_by_id(product_id) is None:
        print("\nProduct not found.\n")
        return
    while True:
        stock_input = input("Enter new stock: ").strip()
        if stock_input.isdigit():
            inventory.update_stock(product_id, int(stock_input))
            print(f"\nUpdated product {product_id} to new stock: {stock_input}\n")
            return
        print("Error: please enter a valid non-negative integer.")


def search_product(inventory):
    query = input("Enter product ID or name to search: ")
    results = inventory.search_product(query)
    if results:
        print("\nSearch Results:")
        for p in results:
            p.display_information()
        print()
    else:
        print("\nNo matching product found.\n")


def display_all(inventory):
    products = inventory.get_all_products()
    if not products:
        print("\nInventory is empty.\n")
        return
    print("\nCurrent Inventory:")
    for p in products:
        p.display_information()
        print(f"    {p.get_fulfilment_info()}")
        if isinstance(p, CanBeShipped):
            print(f"    Shipping cost: ${p.calculate_shipping_cost():.2f}")
    print()


def print_menu():
    print("----- Inventory Menu -----")
    print("1. Display")
    print("2. Add")
    print("3. Update")
    print("4. Search")
    print("5. Save")
    print("6. Exit")


def main():
    inventory = Inventory()
    inventory.load()
    if not inventory.get_all_products():
        inventory.add_product(PhysicalProduct("P001", "Wireless Mouse", 25.50, 2, 0.1))
        inventory.add_product(PhysicalProduct("P002", "Keyboard", 45.00, 1, 0.8))
        inventory.add_product(DigitalProduct("P003", "Antivirus Software", 29.99, 3, 850))

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            inventory.save()
        elif choice == "6":
            inventory.save()
            print(" ")
            print("Program terminated.")
            break
        else:
            print("\nInvalid choice. Please select 1-6.\n")


if __name__ == "__main__":
    main()