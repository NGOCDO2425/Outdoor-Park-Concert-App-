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
def main():
    seating = create_seating()
    print_seating(seating)

if __name__ == "__main__":
    main()
