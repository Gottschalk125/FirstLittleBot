import os
#Kann hier noch raus, logik ist komplett aufgeteilt, lediglich für Docker file das es
# keinen ärger macht solange das noch nicht angepasst ist
#
import alpaca_trade_api as tradeapi
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL")

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version="v2")


SYMBOL = "TSLA"
QTY = 1
ENTRY_PRICE = 0

def get_price(symbol):
    barset = api.get_latest_bar(symbol)
    return float(barset.c)

def fallback_brake(symbol):
    barset = api.get_latest_bar(symbol)
    if(barset < ENTRY_PRICE * 0.9):
        print(f"Verkaufe {QTY} {SYMBOL} zu {price}")
        api.submit_order(
            symbol=SYMBOL,
            qty=QTY,
            side="sell",
            type="market",
            time_in_force="gtc"
        )


def get_position(symbol):
    try:
        return api.get_position(symbol)
    except:
        return None

while True:
    try:
        position = get_position(SYMBOL)
        try:
            position = api.get_position(SYMBOL)
        except:
            pass  # keine Position offen

        price = get_price(SYMBOL)
        #CHECK IF WE HAVE TO SELL BEVOR EVERYTHING IS GONE
        fallback_brake(SYMBOL)

        if not position:
            print(f"Kaufe {QTY} {SYMBOL} zu {price}")
            api.submit_order(
                symbol=SYMBOL,
                qty=QTY,
                side="buy",
                type="market",
                time_in_force="gtc"
            )
            ENTRY_PRICE = price
        else:
            entry_price = ENTRY_PRICE
            if price >= entry_price * 1.0005:  # +0,005 %
                print(f"Verkaufe {QTY} {SYMBOL} zu {price}")
                api.submit_order(
                    symbol=SYMBOL,
                    qty=QTY,
                    side="sell",
                    type="market",
                    time_in_force="gtc"
                )

        time.sleep(0.3)
    except Exception as e:
        print("Fehler:", e)
        time.sleep(0.3)