import json
import os

class Product: 
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

    def to_dict(self):
        return {
            "id": self.__id,
            "name": self.__name,
            "price": self.__price,
            "quantity": self.__quantity
        }

    def display_information(self):
        print(f"ID: {self.__id}, Name: {self.__name}, Price: ${self.__price:.2f}, Quantity: {self.__quantity}")

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

def load_inventory():

    if not os.path.exists(INVENTORY_FILE):
        return []

    with open(INVENTORY_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []

    return [Product(d.get("id"), d.get("name"), d.get("price"), d.get("quantity")) for d in data]

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

def add_product(inventory):

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

    product = Product(product_id, name, price, quantity)
    inventory.add_product(product)
    print(f"\nProduct added: {product_id}, {name}, ${price:.2f}, {quantity}\n")


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
        inventory.add_product(Product("P001", "Wireless Mouse", 25.50, 2))
        inventory.add_product(Product("P002", "Keyboard", 45.00, 1))
        inventory.add_product(Product("P003", "USB Cable", 9.99, 3))

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