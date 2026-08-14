"""Database read/write. sqlite3 ships with Python.

Run:
    uv run --project ../CODE-ALONGS \
        python m0/database.py
"""

import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE IF NOT EXISTS prices (
        symbol TEXT NOT NULL,
        date   TEXT NOT NULL,
        close  REAL NOT NULL,
        PRIMARY KEY (symbol, date))
""")

# #region sql
# Write: always parameterised. Never f-string SQL.
conn.executemany(
    "INSERT OR REPLACE INTO prices VALUES (?, ?, ?)",
    [
        ("AAPL", "2020-05-29", 79.49),
        ("AAPL", "2020-06-01", 80.46),
        ("AAPL", "2020-06-02", 80.83),
    ],
)
conn.commit()

# Read: the last close on or BEFORE a date. Never a
# price the investor's simulated date hasn't reached.
rows = conn.execute(
    "SELECT date, close FROM prices"
    " WHERE symbol = ? AND date <= ?"
    " ORDER BY date DESC LIMIT 1",
    ("AAPL", "2020-06-01"),
)
print(list(rows))
# #endregion sql

conn.close()
