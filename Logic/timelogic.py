import pytz
import time
from datetime import datetime, time as dt_time, timedelta

MARKET_TIMEZONE = pytz.timezone('America/New_York')
MARKET_OPEN = dt_time(9, 30)   # 9:30 Uhr New York Zeit
MARKET_CLOSE = dt_time(16, 0) # 16:00 Uhr New York Zeit

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
