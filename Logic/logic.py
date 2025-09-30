from AlpacaAPI.api import get_price, get_position, buy, sell, get_cash
from Config.config import  SYMBOL, QTY
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

#Hier noch eine Form an Benachrichtigung einbauen damit man das mitbekommt wenn es so weit kommt
def fallback_brake(position):
    barset = get_price(SYMBOL)
    if(barset < ENTRY_PRICE * 0.9 and position != None):
        sell(SYMBOL, QTY)
