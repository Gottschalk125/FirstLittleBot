import sys
import time
from Config.config import SYMBOL, QTY, BuyMax, Buypercent, BuyDifShares
from AlpacaAPI.api import get_price, get_position, buy, sell
from Database.Storage.database import init_db
from FastAPI.api import app
from Logic.logic import should_buy, should_sell, fallback_brake, buymax, buy_percentage, validate_config

ENTRY_PRICE = {}

@app.on_event("startup")
def on_startup():
    init_db()

def process_trade(symbol, qty):
    try:
        position = get_position(symbol)
        price = get_price(symbol)

        fallback_brake(position)

        if should_buy(position):
            print(f"Buying {qty} {symbol} at {price}")
            buy(symbol, qty)
            ENTRY_PRICE[symbol] = price
        elif should_sell(position, price, ENTRY_PRICE.get(symbol, 0)):
            print(f"Selling {qty} {symbol} at {price}")
            sell(symbol, qty)
        else:
            print(f"Holding {symbol}. Current price: {price}")
        time.sleep(0.3)
    except Exception as e:
        print(f"Error with {symbol}: {e}")
        time.sleep(0.3)

while True:
    if not BuyDifShares:
        process_trade(SYMBOL, QTY)
    else:
        for i in range(len(SYMBOL)):
            process_trade(SYMBOL[i], QTY[i])
