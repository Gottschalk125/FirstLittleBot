from AlpacaAPI.api import get_price, get_position, buy, sell, get_cash
from Config.config import SYMBOL, QTY, Percent, BuyMax, Buypercent, BuyDifShares
from Messages.messages import send_warning
from main import ENTRY_PRICE
import pandas as pd

LAST_EMA_STATE = {}

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


def calculate_momentum_indicators(historical_data: pd.DataFrame):
    """Fügt dem DataFrame die benötigten technischen Indikatoren hinzu (EMA 10, 20, 50 & RSI 14)."""

    # 'pandas-ta' benötigt die Close-Preise.
    if historical_data.empty or len(historical_data) < 50:
        print("WARNUNG: Nicht genügend Daten für eine verlässliche Indikatorberechnung.")
        return None

    # 1. EMA-Berechnung
    # Das Modul fügt automatisch Spalten wie 'EMA_10', 'EMA_20' hinzu.
    historical_data.ta.ema(length=10, append=True)
    historical_data.ta.ema(length=20, append=True)
    historical_data.ta.ema(length=50, append=True)

    # 2. RSI-Berechnung
    historical_data.ta.rsi(length=14, append=True)

    return historical_data


def should_buy_momentum(symbol, analyzed_data, current_price, position):
    """
    Kauf-Logik: Prüft auf Trendbestätigung (EMA 50), Crossover (EMA 10/20) und RSI > 50.
    """
    if position:
        return False  # Nur kaufen, wenn keine Position gehalten wird

    if analyzed_data is None:
        return False

    latest = analyzed_data.iloc[-1]

    ema10 = latest['EMA_10']
    ema20 = latest['EMA_20']
    ema50 = latest['EMA_50']
    rsi = latest['RSI_14']

    # Zustand des letzten Ticks aus dem Cache holen
    last_ema_state = LAST_EMA_STATE.get(symbol, {})
    last_ema10 = last_ema_state.get('EMA_10')
    last_ema20 = last_ema_state.get('EMA_20')

    # 1. Speichere den aktuellen Zustand für die nächste Iteration
    LAST_EMA_STATE[symbol] = {'EMA_10': ema10, 'EMA_20': ema20}

    # --- Kaufkriterien prüfen ---

    # Kriterium 1: Langfristiger Trend nach oben (Preis über EMA 50)
    trend_up = (current_price > ema50)

    # Kriterium 2: Crossover (EMA 10 kreuzt EMA 20 von unten nach oben)
    crossover = (
            last_ema10 is not None and
            last_ema20 is not None and
            last_ema10 < last_ema20 and
            ema10 > ema20
    )

    # Kriterium 3: Momentum Bestätigung (RSI zeigt steigenden Schwung)
    strong_momentum = (rsi > 50)

    if trend_up and crossover and strong_momentum:
        return True

    return False


def should_sell_momentum(symbol, analyzed_data, current_price, entry_price):
    """
    Verkaufs-Logik: Prüft auf Stop-Loss ODER Ende des kurzfristigen Momentum (Preis unter EMA 20).
    """
    if analyzed_data is None:
        return False

    latest = analyzed_data.iloc[-1]
    ema20 = latest['EMA_20']

    # --- Verkaufskriterien prüfen ---

    # 1. Stop-Loss (z.B. -3% Verlust)
    loss_percent = (current_price - entry_price) / entry_price
    stop_loss_hit = (loss_percent < -0.03)

    # 2. Haupt-Exit: Preis fällt unter den EMA 20 (Ende des kurzfristigen Schwungs)
    momentum_exit = (current_price < ema20)

    if stop_loss_hit:
        return True

    if momentum_exit:
        return True

    return False

