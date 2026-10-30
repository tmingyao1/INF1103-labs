def main():
    # 1. Initialize the inventory to zero
    total_inventory = 0
    failed_entries = 0

    # 2. Continuous loop asking for stock quantity until user types 'quit'
    while True:
        user_input = input("Enter stock quantity (or 'quit' to finish): ").strip()

        # Exit condition
        if user_input.lower() == "quit":
            break

        # 4. Handle invalid input (non-numeric text)
        is_number = user_input.lstrip("-").isdigit() and user_input not in ("", "-")

        if not is_number:
            print(f"Error: '{user_input}' is not a valid number. Entry rejected.")
            failed_entries += 1
            continue

        # 3. Accept stock values as integers
        quantity = int(user_input)

        # 5. Enforce business rules: reject negative numbers
        if quantity < 0:
            print(f"Error: Negative quantity ({quantity}) is not allowed. Entry rejected.")
            failed_entries += 1
            continue

        # 6. Manage state: keep a running total
        total_inventory += quantity

        # 7. Trigger Overstock Alert using if / elif / else
        remaining_capacity = 500 - total_inventory

        if total_inventory > 500:
            print(f"ALERT: Overstock! Total inventory ({total_inventory}) exceeds 500 units.")
            print(f"Capacity exceeded by {remaining_capacity} units.")  # e.g. -12
            break
        elif total_inventory == 500:
            print(f"Notice: Inventory is exactly at capacity ({total_inventory} units).")
        else:
            print(f"Accepted. Current total inventory: {total_inventory}. Remaining capacity: {remaining_capacity}.")

    # 8. Reporting
    print("\n--- Audit Report ---")
    print(f"Total Units Processed: {total_inventory}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")


if __name__ == "__main__":
    main()