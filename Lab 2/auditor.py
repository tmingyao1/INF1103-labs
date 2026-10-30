# Smart Inventory Auditor

inventory = 0
failed_entries = 0

while True:
    stock = input("Enter stock quantity (or type 'quit' to finish): ")

    # Stop the program if user types quit
    if stock.lower() == "quit":
        break

    # Check if input is a number
    if not stock.isdigit():
        print("Error: Please enter a valid integer.")
        failed_entries += 1
        continue

    # Convert the input from string to integer
    stock = int(stock)

    # Reject negative numbers
    if stock < 0:
        print("Error: Negative numbers are not allowed.")
        failed_entries += 1
        continue

    # Add valid stock to inventory
    inventory += stock

    print("Stock accepted.")
    print("Current inventory:", inventory)

    # Check if inventory exceeds 500
    if inventory > 500:
        print("ALERT: Overstock! Inventory exceeds 500 units.")
        break

# Final report
print("\n--- Final Report ---")
print("Total Units Processed:", inventory)
print("Number of Failed/Rejected Entries:", failed_entries)