import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
import pandas as pd

from Database.ControlDB.trade_repository import repo
from alpaca.data.requests import StockBarsRequest  # <--- HIER sind die fehlenden Klassen
from alpaca.data.timeframe import TimeFrame

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
    repo.add_trade(symbol, qty, get_price(symbol), "buy")

def sell(symbol, qty):
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side="sell",
        type="market",
        time_in_force="gtc"
    )
    repo.add_trade(symbol, qty, get_price(symbol), "sell")

def get_cash():
    account = api.get_account()
    return float(account.cash)

def get_historical_data(symbol, timeframe=TimeFrame.Minute, limit=50):

    request_params = StockBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=timeframe,  # z.B. TimeFrame.Minute
        limit=limit
    )

    bars = api.get_stock_bars(request_params).df

    if not bars.empty:
        return bars.loc[symbol].reset_index(drop=False)

    return pd.DataFrame()