from AlpacaAPI.api import get_price, get_position, buy, sell, get_cash
from Config.config import SYMBOL, QTY, Percent, BuyMax, Buypercent, BuyDifShares
from Messages.messages import send_warning
from main import ENTRY_PRICE

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


