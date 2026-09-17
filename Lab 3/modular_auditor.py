def get_valid_input():
    while True:
        value = input("Enter stock quantity (or type 'quit' to finish): ")

        if value.lower() == "quit":
            return 'quit'

        if not value.isdigit():
            print("Error: Please enter a valid positive integer.")
            continue

        value = int(value)

        if value < 0:
            print("Error: Negative numbers are not allowed.")
            continue

        return value

def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total

def calculate_tax(amount):
    tax = amount * 0.10
    return tax

def generate_report(total_units, failed_attempts):
    print("\n--- Final Report ---")
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)

inventory = 0
failed_attempts = 0

while True:
    delivery = get_valid_input()

    if delivery == 'quit':
        break
    inventory = process_delivery(inventory, delivery)

    tax = calculate_tax(delivery)

    print('Tax for this delivery:', tax)
    print('Current inventory:', inventory)

    if inventory > 500:
        print("ALERT: Overstock! Inventory exceeds 500 units.")
        break

generate_report(inventory, failed_attempts)
