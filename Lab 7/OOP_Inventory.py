import json
import os
from abc import ABC, abstractmethod


class Product(ABC):
    def __init__(self, product_id, name, price, quantity):
        self.__id = product_id
        self.__name = name
        self.__price = price
        self.__quantity = quantity

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def update_stock(self, new_quantity):
        self.__quantity = new_quantity

    @abstractmethod
    def get_fulfilment_info(self):
        pass

    def to_dict(self):
        return {
            "id": self.__id,
            "name": self.__name,
            "price": self.__price,
            "quantity": self.__quantity
        }

    def display_information(self):
        print(f"ID: {self.__id}, Name: {self.__name}, Price: ${self.__price:.2f}, Quantity: {self.__quantity}")


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, quantity, weight):
        super().__init__(product_id, name, price, quantity)
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"    Type: Physical, Weight: {self.__weight} kg")

    def get_fulfilment_info(self):
        return f"{self.get_name()} requires physical shipping."

    def calculate_shipping_cost(self):
        return 3.99 + self.__weight * 1.50

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, quantity, download_size):
        super().__init__(product_id, name, price, quantity)
        self.__download_size = download_size

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()
        print(f"    Type: Digital, Download size: {self.__download_size} MB")

    def get_fulfilment_info(self):
        return f"{self.get_name()} is delivered digitally via a download link."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data


class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        self.__products.append(product)

    def search_product(self, product_id):
        for p in self.__products:
            if p.get_id() == product_id:
                return p
        return None

    def display_all(self):
        if not self.__products:
            print("\nInventory is empty.\n")
            return

        print("\nCurrent Inventory:")
        for p in self.__products:
            p.display_information()
        print()

    def get_all_products(self):
        return self.__products

INVENTORY_FILE = "inventory.json"

def create_product_from_dict(d):
    if d.get("type") == "digital":
        return DigitalProduct(d.get("id"), d.get("name"), d.get("price"),
                              d.get("quantity"), d.get("download_size"))
    return PhysicalProduct(d.get("id"), d.get("name"), d.get("price"),
                           d.get("quantity"), d.get("weight", 0.0))

def load_inventory():

    if not os.path.exists(INVENTORY_FILE):
        return []

    with open(INVENTORY_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []

    return [create_product_from_dict(d) for d in data]

def save_inventory(inventory):
    data = [p.to_dict() for p in inventory.get_all_products()]
    with open(INVENTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print('Saving inventory before exit...')
    print("Inventory saved to inventory.json")

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
        quantity_input = input("Enter quantity: ").strip()
        if quantity_input.isdigit():
            quantity = int(quantity_input)
            break
        print("Error: please enter a valid non-negative integer.")

    if product_type == "1":
        weight = read_positive_float("Enter weight (kg): ")
        product = PhysicalProduct(product_id, name, price, quantity, weight)
    else:
        download_size = read_positive_float("Enter download size (MB): ")
        product = DigitalProduct(product_id, name, price, quantity, download_size)

    inventory.add_product(product)
    print("\nProduct added:")
    product.display_information()
    print()


def update_stock(inventory):
    
    product_id = input("Enter product ID to update: ").strip()
    product = inventory.search_product(product_id)
    if product:
        while True:
            quantity_input = input("Enter new quantity: ").strip()
            if quantity_input.isdigit():
                product.update_stock(int(quantity_input))
                print(f"\nUpdated product {product_id} to new quantity: {quantity_input}\n")
                return
            print("Error: please enter a valid non-negative integer.")
    else:
        print("\nProduct not found.\n")

def search_product(inventory):
    query = input("Enter product ID or name to search: ").strip().lower()

    results = [
        p for p in inventory.get_all_products()
        if query == p.get_id().lower() or query in p.get_name().lower()
    ]

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
    loaded_products = load_inventory()
    if loaded_products:
        for p in loaded_products:
            inventory.add_product(p)
    else:
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
            save_inventory(inventory)
        elif choice == "6":
            save_inventory(inventory)
            print(" ")
            print("Program terminated.")
            break
        else:
            print("\nInvalid choice. Please select 1-6.\n")

if __name__ == "__main__":
    main()