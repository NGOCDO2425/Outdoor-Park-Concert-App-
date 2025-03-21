import json

ROWS, COLS = 20, 26
AVAILABLE, OCCUPIED = "a", "X"
MASK_FEE, TAX_RATE = 5, 0.0725

# Get ticket price
def get_price(row):
    return 80 if row <= 4 else 50 if row <= 10 else 25

# Create empty seating chart
def create_seating():
    return [[AVAILABLE] * COLS for _ in range(ROWS)]

# Load JSON data (create if missing)
def load_data(file, default):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        save_data(default, file)
        return default

# Save data to JSON
def save_data(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# Show seating chart
def print_seating():
    seating = load_data("seating.json", create_seating())
    print("\n   " + " ".join(chr(65 + i) for i in range(COLS)))
    for i, row in enumerate(seating):
        print(f"{i:2} {' '.join(row)}")

# Show available seats
def print_available_seats():
    seating = load_data("seating.json", create_seating())
    available = [f"{r}{chr(c+65)}" for r in range(ROWS) for c in range(COLS) if seating[r][c] == AVAILABLE]
    print("\n✅ Available Seats:", ", ".join(available) if available else "None")

# Check seat availability
def is_seat_available(seating, row, col):
    return 0 <= row < ROWS and 0 <= col < COLS and seating[row][col] == AVAILABLE

# Generate receipt and update accounting
def generate_receipt(name, email, row, col, total):
    receipt = {
        "Name": name,
        "Email": email,
        "Seat": f"{row}{chr(col+65)}",
        "Total Price": f"${total:.2f}"
    }
    print("\n📜 Receipt:")
    for key, value in receipt.items():
        print(f"{key}: {value}")

    # Save to accounting file
    accounting = load_data("accounting.json", [])
    accounting.append(receipt)
    save_data(accounting, "accounting.json")

# Buy ticket function
def buy_ticket():
    seating = load_data("seating.json", create_seating())
    purchases = load_data("purchases.json", {})

    name = input("Name: ")
    email = input("Email: ")
    row = int(input("Row (0-19): "))
    col = ord(input("Col (A-Z): ").upper()) - 65

    if is_seat_available(seating, row, col):
        seating[row][col] = OCCUPIED
        price = get_price(row)
        total = round(price + price * TAX_RATE + MASK_FEE, 2)

        purchases[name] = {"email": email, "seat": f"{row}{chr(col+65)}", "total": total}

        save_data(seating, "seating.json")
        save_data(purchases, "purchases.json")

        print(f"\n✅ {name} booked {row}{chr(col+65)}. Total: ${total:.2f}")

        # Generate receipt and save to accounting
        generate_receipt(name, email, row, col, total)

    else:
        print("\n❌ Seat not available. Try another one.")

# Main menu
def main():
    while True:
        print("\n[V] View Seating  [A] Available Seats  [B] Buy Ticket  [R] Receipts  [Q] Quit")
        choice = input("Choose: ").upper()

        if choice == "V":
            print_seating()
        elif choice == "A":
            print_available_seats()
        elif choice == "B":
            buy_ticket()
        elif choice == "R":
            receipts = load_data("accounting.json", [])
            if receipts:
                print("\n📜 All Receipts:")
                for receipt in receipts:
                    print(receipt)
            else:
                print("\n❌ No purchases yet.")
        elif choice == "Q":
            break
        else:
            print("\n❌ Invalid option, try again.")

if __name__ == "__main__":
    main()
