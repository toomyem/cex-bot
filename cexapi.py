
import json
import urllib
import urllib2
import hmac
import hashlib
import time

class CexApi:

  CEX_API_BASE = "https://cex.io/api/"

  def __init__(self, username, apikey, secret):
    self.username = username
    self.apikey = apikey
    self.secret = secret

  def add_security(self, params):
    nonce = int(time.time())
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
    req = urllib2.Request(uri, params, headers)
    data = urllib2.urlopen(req)
    if data.getcode() != 200 or data.info().gettype() != "text/json":
      raise "Invalid response"
    resp = data.read()
    return json.loads(resp)

  def get_ticker(self):
    return self.req("ticker/GHS/BTC/")

  def get_trade_hist(self, tid = 0):
    params = {}
    if tid > 0: params = {'since': tid}
    return self.req("trade_history/GHS/BTC/", False, params)

  def get_balance(self):
    return self.req("balance/", True)

  def get_open_orders(self):
    return self.req("open_orders/GHS/BTC/", True)

  def cancel_order(self, id):
    return self.req("cancel_order/", True, {'id': id})

  def place_buy_order(self, amount, price):
    return self.req("place_order/GHS/BTC/", True,
      {'type': 'buy', 'amount': amount, 'price': price})

  def place_sell_order(self, amount, price):
    return self.req("place_order/GHS/BTC/", True,
      {'type': 'sell', 'amount': amount, 'price': price})

  def get_workers(self):
    return self.req("ghash.io/workers", True)

  def get_hashrate(self):
    return self.req("ghash.io/hashrate", True)
