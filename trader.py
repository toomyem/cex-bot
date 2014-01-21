
import cexapi
import config
import time
import notify

api = cexapi.CexApi(config.username, config.apikey, config.secret)

def get_last_tid(orders):
  return max([o['id'] for o in orders])

def get_mean_price(orders):
  p = [o['price'] for o in orders]
  return sum(p)/len(p)

def sell_ghs(amount, price):
    if config.debug_mode:
      msg = "You should sell %f GHS for %0.8f BTC on cex.io" % (amount, price)
      print msg
      if config.mail_enabled: notify.send_mail(msg)
      return False
    else:
      msg = "Attempting to sell %f GHS for %0.8f BTC on cex.io" % (amount, price)
      print msg
      print api.place_sell_order(amount, price)
      if config.mail_enabled: notify.send_mail(msg)
      return True

def to8(num):
    return "%0.8f" % num

def get_ts():
    return "[" + time.strftime("%Y/%m/%d %H:%M:%S") + "]"

def trailing_stop_loss(limit, maximum, delay):
  orders = api.get_trade_hist()
  last_tid = get_last_tid(orders)
  last_price = 0

  while True:
    orders = api.get_trade_hist(last_tid)
    last_tid = get_last_tid(orders)
    price = get_mean_price(orders)
    delta = price - last_price
    diff = price - limit

    if price < limit:
      print get_ts(), "price went down to:", to8(price), "limit:", to8(limit)
      if sell_ghs(config.ghs, limit):
        break

    if price > maximum:
      limit += (price - maximum)
      maximum = price

    print get_ts(), "limit:", to8(limit), "price:", to8(price), "max:", to8(maximum), "diff:", to8(diff), "delta:", to8(delta)

    last_price = price
    time.sleep(config.delay)

if __name__ == '__main__':
  trailing_stop_loss(config.limit, config.maximum, config.delay)

