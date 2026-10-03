import json
import os

INVENTORY_FILE = "inventory.json"

def load_inventory():

    if not os.path.exists(INVENTORY_FILE):
        return []

    with open(INVENTORY_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_inventory(inventory):

    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=4)
    print('Saving inventory before exit...')
    print("Inventory saved to inventory.json")

def get_next_product_id(inventory):
    
    highest = 0
    width = 3  # digits after the "P", matches P001 style

    for p in inventory:
        pid = p.get("id", "")
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

    product = {"id": product_id, "name": name, "price": price, "quantity": quantity}
    inventory.append(product)
    print(f"\nProduct added: {product}\n")


def update_stock(inventory):
    
    product_id = input("Enter product ID to update: ").strip()

    for product in inventory:
        if product.get("id") == product_id:
            while True:
                quantity_input = input("Enter new quantity: ").strip()
                if quantity_input.isdigit():
                    product["quantity"] = int(quantity_input)
                    print(f"\nUpdated: {product}\n")
                    return
                print("Error: please enter a valid non-negative integer.")

    print("\nProduct not found.\n")


def search_product(inventory):
    
    query = input("Enter product ID or name to search: ").strip().lower()

    results = [
        p for p in inventory
        if query == p.get("id", "").lower() or query in p.get("name", "").lower()
    ]

    if results:
        print("\nSearch Results:")
        for p in results:
            price = p.get("price", 0.0)
            print(f"ID: {p.get('id')}, Name: {p.get('name')}, "
                  f"Price: ${price:.2f}, Quantity: {p.get('quantity', 0)}")
        print()
    else:
        print("\nNo matching product found.\n")


def display_all(inventory):
    
    if not inventory:
        print("\nInventory is empty.\n")
        return

    print("\nCurrent Inventory:")
    for p in inventory:
        price = p.get("price", 0.0)
        print(f"ID: {p.get('id')}, Name: {p.get('name')}, "
              f"Price: ${price:.2f}, Quantity: {p.get('quantity', 0)}")
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
    
    inventory = load_inventory()

    if not inventory:
        inventory = [
            {"id": "P001", "name": "Wireless Mouse", "price": 25.50, "quantity": 2},
            {"id": "P002", "name": "Keyboard", "price": 45.00, "quantity": 1},
            {"id": "P003", "name": "USB Cable", "price": 9.99, "quantity": 3},
        ]

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