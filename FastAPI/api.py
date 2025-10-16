# FastAPI/api.py

from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
from Database.ControlDB.trade_repository import repo
from AlpacaAPI.api import get_cash
from Config.config import config  # <- neue Zeile!

app = FastAPI()

class ConfigUpdate(BaseModel):
    SYMBOL: Optional[List[str]] = None
    QTY: Optional[List[int]] = None
    BuyMax: Optional[bool] = None
    Buypercent: Optional[bool] = None
    Percent: Optional[float] = None
    BuyDifShares: Optional[bool] = None
    MODE_MOMENTUM: Optional[bool] = None
    MODE_MEAN_REVERSION: Optional[bool] = None
    EMAILUSER: Optional[str] = None


@app.get("/config")
def get_config():
    """Gibt aktuelle Laufzeit-Konfiguration zurück"""
    return config.as_dict()


@app.put("/config")
def update_config(update: ConfigUpdate):
    """Ändert Konfiguration zur Laufzeit"""
    for key, value in update.dict(exclude_unset=True).items():
        setattr(config, key, value)
    return {"message": "Config updated successfully", "config": config.as_dict()}


@app.get("/account/balance")
def get_account_balance():
    return {"cash": get_cash()}


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
    return repo.get_all_trades()


@app.get("/trades/{symbol}")
def get_trades_by_symbol(symbol: str):
    trades = repo.get_trades_by_symbol(symbol)
    return {"symbol": symbol, "trades": trades}


@app.get("/trades/range")
def get_trades_in_range(
    starttime: str = Query(..., description="Startzeit, z. B. 2025-10-07 00:00:00"),
    endtime: str = Query(..., description="Endzeit, z. B. 2025-10-08 00:00:00")
):
    trades = repo.get_trades_in_time_range(starttime, endtime)
    return {"start": starttime, "end": endtime, "trades": trades}
