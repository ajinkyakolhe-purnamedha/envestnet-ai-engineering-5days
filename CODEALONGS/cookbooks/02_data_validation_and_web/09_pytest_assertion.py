# Pytest assertion
def calculate_value(shares, price):
    return shares * price

def test_calculate_value():
    assert calculate_value(10, 250) == 2_500

