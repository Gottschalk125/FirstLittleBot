import sys
import time
from datetime import datetime, time as dt_time
import pytz
from alpaca.data.timeframe import TimeFrame

from Config.config import SYMBOL, QTY, BuyMax, Buypercent, BuyDifShares, MODE_MOMENTUM, MODE_MEAN_REVERSION
from AlpacaAPI.api import get_price, get_position, buy, sell, get_historical_data
from Database.Storage.database import init_db
from FastAPI.api import app
from Logic.tradinglogic import should_buy, should_sell, fallback_brake, buymax, buy_percentage, validate_config, \
    calculate_momentum_indicators, should_sell_momentum, should_buy_momentum
from Logic.timelogic import is_market_open

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

        # Holen und Analysieren der Daten (nur nötig, wenn Momentum aktiv ist)
        analyzed_data = None
        if MODE_MOMENTUM:
            historical_data = get_historical_data(symbol, timeframe=TimeFrame.Minute, limit=50)
            analyzed_data = calculate_momentum_indicators(historical_data)

        fallback_brake(position)

        # ---------------------------------
        # A. VERKAUFS-LOGIK (PRIORITÄT 1)
        # ---------------------------------
        if position:
            sold = False

            # Prüfen auf Momentum-Verkauf (z.B. EMA 20 gebrochen)
            if MODE_MOMENTUM and should_sell_momentum(symbol, analyzed_data, price, ENTRY_PRICE.get(symbol, 0)):
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔴 SELL (Momentum Exit) {qty} {symbol} at {price}")
                sell(symbol, qty)
                sold = True

            # Prüfen auf Standard-Verkauf (z.B. Gewinnziel/Stop-Loss der Dip-Strategie)
            elif MODE_MEAN_REVERSION and should_sell(position, price, ENTRY_PRICE.get(symbol, 0)):
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔴 SELL (Dip Exit) {qty} {symbol} at {price}")
                sell(symbol, qty)
                sold = True

            if not sold:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 🟡 HOLD {symbol}. Price: {price}")

        # ---------------------------------
        # B. KAUF-LOGIK (PRIORITÄT 2)
        # ---------------------------------
        else:
            bought = False

            # 1. Höhere Priorität: Mean Reversion (Dip-Kauf)
            if MODE_MEAN_REVERSION and should_buy(position):
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 🟢 BUY (Dip Entry) {qty} {symbol} at {price}")
                buy(symbol, qty)
                ENTRY_PRICE[symbol] = price
                bought = True

            # 2. Niedrigere Priorität: Momentum (Trend-Kauf)
            elif MODE_MOMENTUM and analyzed_data is not None and should_buy_momentum(symbol, analyzed_data, price,
                                                                                     position):
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 🟢 BUY (Momentum Entry) {qty} {symbol} at {price}")
                buy(symbol, qty)
                ENTRY_PRICE[symbol] = price
                bought = True

            if not bought:
                print(
                    f"[{datetime.now().strftime('%H:%M:%S')}] 🟡 HOLD {symbol}. Current price: {price}. Kein Kaufsignal.")

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
