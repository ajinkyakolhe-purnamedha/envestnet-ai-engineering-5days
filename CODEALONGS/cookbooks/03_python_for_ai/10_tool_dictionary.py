# Tool dictionary
def get_price():
    return 228.80

def get_cash():
    return 25_000

TOOLS = {"price": get_price, "cash": get_cash}
print(TOOLS["price"]())

