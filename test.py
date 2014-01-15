
import cexapi

api = cexapi.CexApi("toomyem", "apikey", "secret")
print api.get_balance()
#print api.get_ticker()
#print api.place_buy_order(0.001, 0.042)
#print api.get_open_orders()
#print api.cancel_order(192780330)
#print api.get_workers()
#print api.get_hashrate()

