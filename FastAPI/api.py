from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
from Database.ControlDB.trade_repository import repo
from AlpacaAPI.api import get_cash

app = FastAPI()

config = {
    "SYMBOL": [],
    "QTY": [],
    "BuyMax": False,
    "Buypercent": False,
    "Percent": 0.0,
    "BuyDifShares": False
}

account_balance = get_cash()

class ConfigUpdate(BaseModel):
    SYMBOL: Optional[List[str]] = None
    QTY: Optional[List[int]] = None
    BuyMax: Optional[float] = None
    Buypercent: Optional[float] = None
    Percent: Optional[float] = None
    BuyDifShares: Optional[bool] = None

@app.put("/config")
def update_config(update: ConfigUpdate):
    for key, value in update.dict(exclude_unset=True).items():
        config[key] = value
    return {"message": "Config updated successfully", "config": config}

@app.get("/config")
def get_config():
    return config

@app.get("/account/balance")
def get_account_balance():
    account_balance = get_cash()
    return account_balance

trading_status = {"running": False}

@app.post("/start")
def start_trading():
    trading_status["running"] = True
    return {"message": "Trading started", "status": trading_status}

@app.post("/stop")
def stop_trading():
    trading_status["running"] = False
    return {"message": "Trading stopped", "status": trading_status}

@app.get("/trades")
def get_all_trades():
    trades = repo.get_all_trades()
    return trades

@app.get("/trades/{symbol}")
def get_trades_by_symbol(symbol: str):
    """Trades für ein bestimmtes Symbol"""
    trades = repo.get_trades_by_symbol(symbol)
    return {"symbol": symbol, "trades": trades}


@app.get("/trades/range")
def get_trades_in_range(
    starttime: str = Query(..., description="Startzeit, z.B. 2025-10-07 00:00:00"),
    endtime: str = Query(..., description="Endzeit, z.B. 2025-10-08 00:00:00")
):
    """Trades in einem bestimmten Zeitbereich abrufen"""
    trades = repo.get_trades_in_time_range(starttime, endtime)
    return {"start": starttime, "end": endtime, "trades": trades}
