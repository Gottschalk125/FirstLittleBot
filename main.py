import time
from Config.config import  SYMBOL, QTY
from APICalls.api import get_price, get_position, buy, sell
from Logic.logic import should_buy, should_sell, fallback_brake

ENTRY_PRICE = 0

while True:
    try:
        position = get_position(SYMBOL)
        price = get_price(SYMBOL)

        fallback_brake(position)

        if should_buy(position):
            print(f"Buying {QTY} {SYMBOL} at {price}")
            buy(SYMBOL, QTY)
            ENTRY_PRICE = price
        elif should_sell(position, price, ENTRY_PRICE):
            print(f"Selling {QTY} {SYMBOL} at {price}")
            sell(SYMBOL, QTY)
        else :
            print(f"Holding {SYMBOL}. Current price: {price}")
        time.sleep(0.3)
    except Exception as e:
        print("Fehler:", e)
        time.sleep(0.3)
