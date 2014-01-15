
import cexapi
import time

#################################################################
# data needed to access cex.io api
username = ""
apikey = ""
secret = ""

# settings about trade ------------------------------------------
stop_loss = 0.001     # how match are you willing to loose?
take_profit = 0.02    # level to escape when price suddenly drops
start_ghs = 1.35      # how many ghs do you want to trade
start_price = 0.04575 # price you paid for those ghashes

#################################################################

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
    
  def watch(self, ghs, price, stop_loss, take_profit):
    self.last_tid = 0
    self.get_trade_data()  # initialize last_tid
    
    max_val = 0
    stop_price = price * (1-stop_loss)
    sell_price = stop_price * 0.999

    while True:
      try:
        data = self.get_trade_data()
      except urllib2.HTTPError as ex:
        print ex
        time.sleep(5)
        continue
        
      val = self.get_mean_value(data)
      diff = val - price
      gain = val/price
      max_val = max(val, max_val)
      drop_size = max_val * take_profit
      drop = max_val - val
      
      print "[%s] val: %0.8f (%0.08f), drop: %0.8f (%0.8f), max: %0.8f, gain: %0.8f, diff: %0.8f" \
        % (get_ts(), val, stop_price, drop, drop_size, max_val, gain, diff)

      if val <= stop_price:
        if self.sell(ghs, sell_price, "Stop loss!"): break
      if drop >= drop_size:
        if self.sell(ghs, sell_price, "Sell at top!"): break

      time.sleep(15)

  def sell(self, amount, price, msg):
    print msg
    result = self.api.place_sell_order(amount, price)
    print result
    return True
    
#################################

api = cexapi.CexApi(username, apikey, secret)
trader = Trader(api)
trader.watch(start_ghs, start_price, stop_loss, take_profit)


