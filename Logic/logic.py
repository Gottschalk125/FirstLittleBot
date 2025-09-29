def should_buy(position):
    return position is None

#Need to fix here
def should_sell(position, price, entry_price):
    return price >= entry_price * 1.0005