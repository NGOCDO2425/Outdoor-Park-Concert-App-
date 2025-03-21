import json

ROWS, COLS = 20, 26
AVAILABLE, OCCUPIED = "a", "X"
MASK_FEE, TAX_RATE = 5, 0.0725

# Ticket price by row
def get_price(row):
    return 80 if row <= 4 else 50 if row <= 10 else 25

# Create seating
def create_seating():
    return [[AVAILABLE] * COLS for _ in range(ROWS)]

# Load JSON data, create file if not found
def load_data(file, default):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        save_data(default, file)
        return default

# Save data to JSON file
def save_data(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# Show seating chart
def print_seating():
    seating = load_data("seating.json", create_seating())  
    print("\n   " + " ".join(chr(65 + i) for i in range(COLS)))
    for i, row in enumerate(seating):
        print(f"{i:2} {' '.join(row)}")

# Show available seats only
def print_available_seats():
    seating = load_data("seating.json", create_seating())  
    available_seats = [f"{r}{chr(c+65)}" for r in range(ROWS) for c in range(COLS) if seating[r][c] == AVAILABLE]

    if available_seats:
        print("\n✅ Available Seats:\n" + ", ".join(available_seats))
    else:
        print("\n❌ No available seats left.")

# Check seat availability
def is_seat_available(seating, row, col):
    return 0 <= row < ROWS and 0 <= col < COLS and seating[row][col] == AVAILABLE

# Buy one seat
def buy_single():
    # Load latest data
    seating = load_data("seating.json", create_seating())
    purchases = load_data("purchases.json", {})

    # Get user input
    name = input("Name: ")
    email = input("Email: ")
    row = int(input("Row (0-19): "))
    col = ord(input("Col (A-Z): ").upper()) - 65

    # Check seat availability before purchase
    if is_seat_available(seating, row, col):
        seating[row][col] = OCCUPIED
        price = get_price(row)
        total = round(price + price * TAX_RATE + MASK_FEE, 2)

        # Store purchase details
        purchases[name] = {"email": email, "seat": f"{row}{chr(col+65)}", "total": total}

        # Save updated seating and purchases
        save_data(seating, "seating.json")
        save_data(purchases, "purchases.json")

        print(f"\n✅ Booked {row}{chr(col+65)}. Total: ${total:.2f}")
    else:
        print("\n❌ Seat not available. Try another one.")

# Main menu
def main():
    while True:
        print("\n[V] View Seating  [A] Available Seats  [B] Buy Ticket  [Q] Quit")
        choice = input("Choose: ").upper()

        if choice == "V":
            print_seating()
        elif choice == "A":
            print_available_seats()
        elif choice == "B":
            buy_single()
        elif choice == "Q":
            break
        else:
            print("\n❌ Invalid option, try again.")

if __name__ == "__main__":
    main()
