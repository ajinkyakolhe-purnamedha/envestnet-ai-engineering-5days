# Exception handling
try:
    price = float("not-a-price")
except ValueError:
    print("Invalid price")

