from AlpacaAPI.api import get_price, get_position, buy, sell, get_cash
from Config.config import SYMBOL, QTY, Percent, BuyMax, Buypercent, BuyDifShares
from Messages.messages import send_warning
from main import ENTRY_PRICE
import pytz
import time
from datetime import datetime, time as dt_time, timedelta
import sys

MARKET_TIMEZONE = pytz.timezone('America/New_York')
MARKET_OPEN = dt_time(9, 30)   # 9:30 Uhr New York Zeit
MARKET_CLOSE = dt_time(16, 0) # 16:00 Uhr New York Zeit

def should_buy(position):
    return position is None

def should_sell( price, entry_price):
    return price >= entry_price * 1.0005

def buymax(position):
    cash = get_cash()
    price = get_price(SYMBOL)
    max_qty: int = int(cash // price)
    if max_qty > 0 and position is None:
        buy(SYMBOL, max_qty)
        QTY = max_qty
        return max_qty
    return 0

def buy_percentage(position):
    if(Percent <= 0 or Percent > 1):
        raise ValueError("Percent must be between 0 and 1")
    cash = get_cash() * Percent
    price = get_price(SYMBOL)
    max_qty: int = int(cash // price)
    if max_qty > 0 and position is None:
        buy(SYMBOL, max_qty)
        QTY = max_qty
        return max_qty
    return 0

def validate_config():
    if not isinstance(SYMBOL, list) or not isinstance(QTY, list):
        BuyDifShares = False
        raise ValueError("SYMBOL and QTY must both be lists.")
    if len(SYMBOL) != len(QTY):
        BuyDifShares = False
        raise ValueError("SYMBOL and QTY must have the same number of elements.")
    if isinstance(SYMBOL, list) or isinstance(QTY, list):
        BuyMax = False
        Buypercent = False
        BuyDifShares = True
    if(QTY <= 0):
        raise ValueError("QTY must be greater than 0")
    if(Percent <= 0 or Percent > 1):
        raise ValueError("Percent must be between 0 and 1")
    if(SYMBOL == ""):
        raise ValueError("SYMBOL must be set")
    if (BuyMax and Buypercent):
        raise ValueError("BuyMax and Buypercent cannot be both true")

def fallback_brake(position):
    barset = get_price(SYMBOL)
    if(barset < ENTRY_PRICE * 0.9 and position != None):
        sell(SYMBOL, QTY)
        send_warning(position)


def is_market_open():
    now_nyc = datetime.now(MARKET_TIMEZONE)
    if now_nyc.weekday() >= 5:
        print(f"Markt geschlossen. Heute ist {now_nyc.strftime('%A')}.")
        return False

    current_time = now_nyc.time()

    if MARKET_OPEN <= current_time < MARKET_CLOSE:
        return True
    else:
        return False


def get_today_timestamp_range():

    today = datetime.now().date()


    start_of_day = datetime.combine(today, time.min)

    end_of_day = datetime.combine(today, time.max)

    start_ts_str = start_of_day.strftime('%Y-%m-%d %H:%M:%S')
    end_ts_str = end_of_day.strftime('%Y-%m-%d 23:59:59')

    return start_ts_str, end_ts_str
