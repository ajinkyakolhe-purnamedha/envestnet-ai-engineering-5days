# Filter a DataFrame
import pandas as pd

prices = pd.DataFrame({"symbol": ["SPY", "QQQ", "GLD"], "price": [228.80, 170.70, 140.11]})
spy_price = prices[prices["symbol"] == "SPY"]
print(spy_price)

