from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

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