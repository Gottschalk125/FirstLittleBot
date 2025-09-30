import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL")
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version="v2")

def get_price(symbol):
    bar = api.get_latest_bar(symbol)
    return float(bar.c)

def get_position(symbol):
    try:
        return api.get_position(symbol)
    except Exception:
        return None

def buy(symbol, qty):
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side="buy",
        type="market",
        time_in_force="gtc"
    )

def sell(symbol, qty):
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side="sell",
        type="market",
        time_in_force="gtc"
    )

def get_cash():
    account = api.get_account()
    return float(account.cash)