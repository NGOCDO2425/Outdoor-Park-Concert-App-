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

# Load/save
def load_data(file, default):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        save_data(default, file)
        return default

def save_data(data, file):
    with open(file, "w") as f:
        json.dump(data, f)

# Show seating
def print_seating(seating):
    print("\n   " + " ".join(chr(65 + i) for i in range(COLS)))
    for i, row in enumerate(seating):
        print(f"{i:2} {' '.join(row)}")

# Social distancing check
def is_seat_available(seating, row, col):
    if seating[row][col] != AVAILABLE:
        return False
    for r in range(row - 2, row + 3):
        for c in range(col - 2, col + 3):
            if 0 <= r < ROWS and 0 <= c < COLS and seating[r][c] == OCCUPIED:
                return False
    return True

# Find block for group
def find_available_block(seating, row, count):
    for col in range(COLS - count):
        if all(is_seat_available(seating, row, col + i) for i in range(count)):
            return col
    return None

# Buy one seat
def buy_single(seating, purchases):
    name, email = input("Name: "), input("Email: ")
    row = int(input("Row (0-19): "))
    col = ord(input("Col (A-Z): ").upper()) - 65
    if is_seat_available(seating, row, col):
        seating[row][col] = OCCUPIED
        price = get_price(row)
        total = price + price * TAX_RATE + MASK_FEE
        purchases[name] = {"email": email, "seat": f"{row}{chr(col+65)}", "total": round(total, 2)}
        save_data(seating, "seating.json")
        save_data(purchases, "purchases.json")
        print(f"Booked {row}{chr(col+65)}. Total: ${total:.2f}")
    else:
        print("Seat not available.")

# Buy group seats
def buy_group(seating, purchases):
    name, email = input("Name: "), input("Email: ")
    row, count = int(input("Row (0-19): ")), int(input("#Tickets: "))
    start = find_available_block(seating, row, count)
    if start is not None:
        seats = [f"{row}{chr(start + i + 65)}" for i in range(count)]
        for i in range(count):
            seating[row][start + i] = OCCUPIED
        price = get_price(row) * count
        total = price + price * TAX_RATE + MASK_FEE
        purchases[name] = {"email": email, "seats": seats, "total": round(total, 2)}
        save_data(seating, "seating.json")
        save_data(purchases, "purchases.json")
        print(f"Booked seats: {', '.join(seats)}. Total: ${total:.2f}")
    else:
        print("No space for group.")

# Search purchase
def search_purchase(purchases):
    name = input("Search name: ")
    if name in purchases:
        print(purchases[name])
    else:
        print("Not found.")

# Show all
def show_all(purchases):
    total = 0
    for name, info in purchases.items():
        seats = info.get("seats", info.get("seat"))
        print(f"{name}: {seats} | ${info['total']:.2f}")
        total += info['total']
    print(f"Total revenue: ${total:.2f}")

# Main menu
def main():
    seating = load_data("seating.json", create_seating())
    purchases = load_data("purchases.json", {})
    while True:
        print("\n[V] View  [B] Buy  [G] Group  [S] Search  [D] Display  [Q] Quit")
        c = input("Choose: ").upper()
        if c == "V": print_seating(seating)
        elif c == "B": buy_single(seating, purchases)
        elif c == "G": buy_group(seating, purchases)
        elif c == "S": search_purchase(purchases)
        elif c == "D": show_all(purchases)
        elif c == "Q": break

main()