import sys
import time
from datetime import datetime, time as dt_time
import pytz

from Config.config import SYMBOL, QTY, BuyMax, Buypercent, BuyDifShares
from AlpacaAPI.api import get_price, get_position, buy, sell
from Database.Storage.database import init_db
from FastAPI.api import app
from Logic.logic import should_buy, should_sell, fallback_brake, buymax, buy_percentage, validate_config, is_market_open

ENTRY_PRICE = {}
MARKET_TIMEZONE = pytz.timezone('America/New_York')
MARKET_OPEN = dt_time(9, 30)  # 9:30 Uhr ET
MARKET_CLOSE = dt_time(16, 0)  # 16:00 Uhr ET


@app.on_event("startup")
def on_startup():
    init_db()


def process_trade(symbol, qty):
    try:
        position = get_position(symbol)
        price = get_price(symbol)

        fallback_brake(position)

        if should_buy(position):
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🟢 BUY {qty} {symbol} at {price}")
            buy(symbol, qty)
            ENTRY_PRICE[symbol] = price
        elif should_sell(position, price, ENTRY_PRICE.get(symbol, 0)):
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔴 SELL {qty} {symbol} at {price}")
            sell(symbol, qty)
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🟡 HOLD {symbol}. Price: {price}")

        time.sleep(0.3)

    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Error with {symbol}: {e}")
        time.sleep(0.3)


def main_loop():
    print("--- Trading Bot gestartet ---")
    while True:
        if is_market_open():

            if BuyDifShares and isinstance(SYMBOL, list) and isinstance(QTY, list):
                for i in range(len(SYMBOL)):
                    process_trade(SYMBOL[i], QTY[i])
            elif not BuyDifShares:
                process_trade(SYMBOL, QTY)
            else:
                print("FEHLER: BuyDifShares ist True, aber SYMBOL/QTY sind keine Listen.")
                time.sleep(60)  # Warte eine Minute bei Konfigurationsfehler

        else:

            print(
                f"\nMarkt geschlossen. Warte 5 Minuten. Aktuelle lokale Zeit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            time.sleep(5 * 60)  # Warte 5 Minuten


if __name__ == "__main__":
    main_loop()
