
import cexapi
import config
import time
import notify

api = cexapi.CexApi(config.username, config.apikey, config.secret)

def get_ts():
    return "[" + time.strftime("%Y/%m/%d %H:%M:%S") + "]"

def log(msg):
  print get_ts(), msg
  if config.log_filename:
    f = open(config.log_filename, "a")
    f.write(get_ts() + " " + msg + "\n")
    f.close()

def get_mean_price(orders):
  p = [o['price'] for o in orders]
  return sum(p)/len(p)

def sell_ghs(amount, price):
    if config.debug_mode:
      msg = "You should sell %f GHS for %0.8f BTC on cex.io" % (amount, price)
      log(msg)
      if config.mail_enabled: notify.send_mail(msg)
      return False
    else:
      msg = "Attempting to sell %f GHS for %0.8f BTC on cex.io" % (amount, price)
      log(msg)
      r = api.place_sell_order(amount, price)
      log(r)
      if config.mail_enabled: notify.send_mail(msg + "\r\n" + r)
      return True

def to8(num):
    return "%0.8f" % round(num, 8)

def trailing_stop_loss(limit, maximum, delay):
  last_price = 0
  start_limit = limit

  while True:
    orders = api.get_trade_hist(since = int(time.time())-config.window)
    if len(orders) == 0:
      price = last_price
    else:
      price = get_mean_price(orders)

    if last_price == 0: last_price = price

    delta = price - last_price
    diff = price - start_limit

    if price < limit:
      log("price went down to: " + to8(price) + " limit: " + to8(limit))
      if sell_ghs(config.ghs, start_limit):
        break

    if price > maximum:
      limit += (price - maximum)
      maximum = price

    log("limit: " + to8(limit) + " price: " + to8(price) + " max: " + to8(maximum) + " diff: " + to8(diff) + " delta: " + to8(delta))

    last_price = price
    time.sleep(config.delay)

if __name__ == '__main__':
  trailing_stop_loss(config.limit, config.maximum, config.delay)

