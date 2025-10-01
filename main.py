import sys
import time
from Config.config import SYMBOL, QTY, BuyMax, Buypercent, BuyDifShares
from AlpacaAPI.api import get_price, get_position, buy, sell
from Logic.logic import should_buy, should_sell, fallback_brake, buymax, buy_percentage, validate_config

ENTRY_PRICE = 0

try:
    validate_config()
except ValueError as e:
    print(f"Config error: {e}")
    sys.exit(1)

while True:
    if(BuyDifShares == False):
        try:
            position = get_position(SYMBOL)
            price = get_price(SYMBOL)

            fallback_brake(position)

            if should_buy(position):
                if(BuyMax):
                    print(f"Buying {QTY} {SYMBOL} at {price}")
                    buymax(position)
                if(Buypercent):
                    print(f"Buying {QTY} {SYMBOL} at {price}")
                    buy_percentage(position)
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
    if(BuyDifShares):
        for i in range(len(SYMBOL)):
            try:
                position = get_position(SYMBOL[i])
                price = get_price(SYMBOL[i])

                fallback_brake(position)

                if should_buy(position):
                    print(f"Buying {QTY[i]} {SYMBOL[i]} at {price}")
                    buy(SYMBOL[i], QTY[i])
                    ENTRY_PRICE = price
                elif should_sell(position, price, ENTRY_PRICE):
                    print(f"Selling {QTY[i]} {SYMBOL[i]} at {price}")
                    sell(SYMBOL[i], QTY[i])
                else :
                    print(f"Holding {SYMBOL[i]}. Current price: {price}")
                time.sleep(0.3)
            except Exception as e:
                print("Fehler:", e)
                time.sleep(0.3)
