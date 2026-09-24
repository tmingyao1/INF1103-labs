import os

INVENTORY_FILE = "inventory.txt"

def load_inventory():
    orders = []
    history = []

    if not os.path.exists(INVENTORY_FILE):
        return orders, history

    with open(INVENTORY_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    section = None
    for line in lines:
        if line == "ORDERS":
            section = "orders"
            continue
        elif line == "HISTORY":
            section = "history"
            continue

        if section == "orders":
            order_id, name, qty = line.split(",")
            orders.append([order_id, name, int(qty)])
        elif section == "history":
            history.append(int(line))

    return orders, history

def save_inventory(orders, history):
    with open(INVENTORY_FILE, "w") as f:
        f.write("ORDERS\n")
        for order_id, name, qty in orders:
            f.write(f"{order_id},{name},{qty}\n")

        f.write("HISTORY\n")
        for amount in history:
            f.write(f"{amount}\n")

def get_next_id(orders):
    if not orders:
        return "1001"
    last_id = int(orders[-1][0])
    return str(last_id + 1)

def get_valid_order(orders):
    while True:
        name = input("Enter Product Name: ").strip()

        if name.lower() == "quit":
            return "quit"

        qty_input = input("Enter Quantity: ").strip()

        if qty_input.lower() == "quit":
            return "quit"

        if not qty_input.isdigit():
            print("Error: Please enter a valid positive integer for quantity.\n")
            continue

        quantity = int(qty_input)

        if quantity < 0:
            print("Error: Negative numbers are not allowed.\n")
            continue

        return name, quantity

def print_orders(orders):
    print("Current Orders:\n")
    for order_id, name, qty in orders:
        print(f"{order_id}, {name}, {qty}")

def generate_report(orders, history, failed_attempts):
    print("\n--- Final Report ---")
    print("Total Orders:", len(orders))
    print("Total Units Ordered:", sum(history))
    print("Number of Failed/Rejected Entries:", failed_attempts)

orders, history = load_inventory()
failed_attempts = 0

while True:
    print_orders(orders)
    print()

    result = get_valid_order(orders)

    if result == "quit":
        save_inventory(orders, history)
        print("\nOrder successfully saved to inventory.txt")
        break

    name, quantity = result
    new_id = get_next_id(orders)
    orders.append([new_id, name, quantity])

    history.append(quantity)

    print(f"\nNew Order Added:\n{new_id},{name},{quantity}\n")

generate_report(orders, history, failed_attempts)