import sqlite3


connection = sqlite3.connect(":memory:")
connection.execute("CREATE TABLE prices (symbol TEXT, date TEXT, close REAL)")
connection.execute("INSERT INTO prices VALUES (?, ?, ?)", ("AAPL", "2020-06-01", 80.46))
row = connection.execute(
    "SELECT close FROM prices WHERE symbol = ? AND date <= ? "
    "ORDER BY date DESC LIMIT 1",
    ("AAPL", "2020-06-01"),
).fetchone()
print(f"AAPL close on 2020-06-01: {row[0]}")
