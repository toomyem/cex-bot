
import cexapi
import config
import time

api = cexapi.CexApi(config.username, config.apikey, config.secret)

def get_last_tid(orders):
  return max([o['id'] for o in orders])

def get_mean_price(orders):
  p = [o['price'] for o in orders]
  return sum(p)/len(p)

def sell_ghs(amount, price):
    print "Sell", amount, "ghs at", to8(price), "btc"
    if not config.debug_mode:
      print api.place_sell_order(amount, price)

def to8(num):
    return "%0.8f" % num

def get_ts():
    return "[" + time.strftime("%Y/%m/%d %H:%M:%S") + "]"

orders = api.get_trade_hist()
last_tid = get_last_tid(orders)
last_price = 0
maximum = config.maximum
limit = config.limit

while True:
  orders = api.get_trade_hist(last_tid)
  last_tid = get_last_tid(orders)
  price = get_mean_price(orders)
  delta = price - last_price

  if price < limit:
    sell_ghs(config.ghs, price)
    break

  if price > maximum:
    limit += price - maximum
    maximum = price

  print get_ts(), "limit:", to8(limit), "price:", to8(price), "max:", to8(maximum), "delta:", to8(delta)

  last_price = price
  time.sleep(config.delay)

