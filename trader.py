
import cexapi
import time
import config

def log(msg):
  print msg
  return False

def get_ts():
  return time.strftime("%Y/%m/%d %H:%M:%S")

#def get_balance():
#  balance = api.get_balance()
#  return (float(balance['GHS']['available']),float(balance['BTC']['available']))
#
#ghs, btc = get_balance()
#print "GHS: %0.8f" % ghs
#print "BTC: %0.8f" % btc


class Trader:

  def __init__(self, api):
    self.api = api
    
  def get_max_tid(self, data):
    return max([x['tid'] for x in data])

  def get_mean_value(self, data):
    values = [float(x['price']) for x in data]
    return sum(values)/len(values)
    
  def get_trade_data(self):
    data = self.api.get_trade_hist(self.last_tid)
    self.last_tid = self.get_max_tid(data)
    return data
    
  def watch(self, ghs, start_price, stop_loss, take_profit):
    self.last_tid = 0
    self.get_trade_data()  # initialize last_tid
    
    max_price = 0
    stop_price = start_price * (1-stop_loss)
    sell_price = stop_price * (1-0.001)

    while True:
      try:
        data = self.get_trade_data()
      except urllib2.HTTPError as ex:
        print ex
        time.sleep(5)
        continue
        
      price = self.get_mean_value(data)
      max_price = max(price, max_price)
      max_drop = max_price * take_profit
      drop = max_price - price
      diff = price - start_price
      gain = price / start_price
      
      print "[%s] price: %0.8f (%0.8f), drop: %0.8f (%0.8f), max: %0.8f, diff: %0.8f, gain: %0.8f" \
        % (get_ts(), price, stop_price, drop, max_drop, max_price, diff, gain)

      if price <= stop_price:
        if self.sell(ghs, sell_price, "Stop loss"): break
      if drop >= max_drop:
        if self.sell(ghs, sell_price, "Sell at top"): break

      time.sleep(20)

  def sell(self, amount, price, msg):
    print "%s, sell price: %0.8f" % (msg, price)
    if config.debug_mode: return False
    result = self.api.place_sell_order(amount, price)
    print result
    return True
    
#################################

if config.debug_mode: print "Debug mode ON!"
api = cexapi.CexApi(config.username, config.apikey, config.secret)
trader = Trader(api)
trader.watch(config.start_ghs, config.start_price, config.stop_loss, config.take_profit)


