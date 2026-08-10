# FastAPI route
from fastapi import FastAPI

app = FastAPI()

@app.get("/price/{symbol}")
def get_price(symbol: str):
    return {"symbol": symbol, "price": 228.80}

