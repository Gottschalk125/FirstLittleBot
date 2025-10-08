from Database.Storage.database import get_connection


def add_trade(self, symbol:str, qty:int, price:float, side:str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO trades (symbol, qty, price, side)
        VALUES (?, ?, ?, ?)
    """, (symbol, qty, price, side))
    conn.commit()
    conn.close()

def get_all_trades(self):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM trades")
    trades = c.fetchall()
    conn.close()
    return trades

def get_trades_by_symbol(self, symbol:str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM trades WHERE symbol = ?", (symbol,))
    trades = c.fetchall()
    conn.close()
    return trades

def get_trades_in_time_range(self, starttime:str, endtime:str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM trades WHERE timestamp BETWEEN ? AND ?", (starttime, endtime))
    trades = c.fetchall()
    conn.close()
    return trades