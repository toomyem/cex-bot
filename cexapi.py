
import json
import urllib
import urllib2
import hmac
import hashlib
import time

def _map_order(o):
  return {'id': int(o['id']),
          'type': str(o['type']),
          'amount': float(o['amount']),
          'price': float(o['price']),
          'time': int(o['time'])/1000, # cex gives time in ms
          'pending': float(o['pending'])}

def _map_hist(h):
    return {'id': int(h['tid']),
            'type': 'unknown',
            'amount': float(h['amount']),
            'price': float(h['price']),
            'time': int(h['date'])}

def _map_book(o):
  return {'price': float(o[0]), 'amount': float(o[1])}


class CexApi:

  CEX_API_BASE = "https://cex.io/api/"

  def __init__(self, username, apikey, secret):
    self.username = username
    self.apikey = apikey
    self.secret = secret

  def get_nonce(self):
    return int(time.time()*1000)

  def set_trading_pair(self, asset, currency):
    raise CexException("setting trading pair is not supported on cex.io")

  def get_trading_pair(self):
    return ("GHS", "BTC")

  def add_security(self, params):
    nonce = self.get_nonce()
    message = str(nonce) + self.username + self.apikey
    sig = hmac.new(self.secret, msg=message, digestmod=hashlib.sha256).hexdigest().upper()
    params['key'] = self.apikey
    params['signature'] = sig
    params['nonce'] = nonce

  def req(self, method, secure = False, extra_params = None):
    uri = self.CEX_API_BASE + method
    params = {}
    if secure: self.add_security(params)
    if extra_params: params.update(extra_params)
    params = urllib.urlencode(params)
    headers = { "User-Agent" : "bot-cex.io" }
    data = None
    while not data:
      try:
        req = urllib2.Request(uri, params, headers)
        data = urllib2.urlopen(req)
      except urllib2.HTTPError as ex:
        print ex
      
    if data.getcode() != 200 or data.info().gettype() != "text/json":
      resp = {'error': 'invalid response'}
    else:
      resp = data.read()
    return json.loads(resp)

  def get_ticker(self):
    t = self.req("ticker/GHS/BTC/")
    return {'volume': float(t['volume']),
            'last': float(t['last']),
            'bid': float(t['bid']),
            'ask': float(t['ask']),
            'low': float(t['low']),
            'high': float(t['high']),
            'time': int(t['timestamp'])}

  def get_trade_hist(self, since = 0):
    hist = self.req("trade_history/GHS/BTC/")
    if since > 0:
      hist = filter(lambda h: int(h['date']) > since, hist)
    return sorted([_map_hist(h) for h in hist], key=lambda h: h['time'])

  def get_balance(self):
    b = self.req("balance/", True)
    asset,currency = self.get_trading_pair()
    return ((float(b[asset]['available']), float(b[asset]['orders'])),
            (float(b[currency]['available']), float(b[currency]['orders'])))

  def get_order_book(self):
    orders = self.req("order_book/GHS/BTC/")
    return {'asks':[_map_book(o) for o in orders['asks']], 
            'bids':[_map_book(o) for o in orders['bids']]}

  def get_open_orders(self):
    orders = self.req("open_orders/GHS/BTC/", True)
    return [_map_order(o) for o in orders]

  def cancel_order(self, id):
    r = self.req("cancel_order/", True, {'id': id})
    return type(r) == bool and r == True

  def place_buy_order(self, amount, price):
    o = self.req("place_order/GHS/BTC/", True,
      {'type': 'buy', 'amount': amount, 'price': round(price,8)})
    if o.has_key('error'): return {'error': o['error']}
    return _map_order(o)

  def place_sell_order(self, amount, price):
    o = self.req("place_order/GHS/BTC/", True,
      {'type': 'sell', 'amount': amount, 'price': round(price,8)})
    if o.has_key('error'): return {'error': o['error']}
    return _map_order(o)
