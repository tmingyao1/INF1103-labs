def main():
    total_inventory = 0
    failed_entries = 0

    while True:
        user_input = input("Enter the stock quantity (or type 'quit' to finish): ").strip()
        if user_input.lower() == 'quit':
            break
        is_number = user_input.lstrip('-').isdigit() and user_input not in ("", "-")

        if not is_number:
          print(f"Error: '{user_input}' is not a valid number. Entry rejected.")
          failed_entries += 1
          continue

        quantity = int(user_input)

        if quantity < 0:
          print(f"Error: Negative quantity ({quantity}) is not allowed. Entry rejected.")
          failed_entries += 1
          continue

        total_inventory += quantity
        print(f"Accepted. Current total inventory: {total_inventory}")

        if total_inventory > 500:
            print(f"ALERT: Overstock! Total inventory ({total_inventory}) exceeds 500 units.")
            break

    print('\n--- Audit Report ---')
    print(f"Total units processed: {total_inventory}")
    print(f"Number of failed/rejected entries: {failed_entries}")

if __name__ == "__main__":
    main()