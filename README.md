cex-bot
=======
Bot to ease the pain of speculation on CEX.io exchange.

usage
=====
Buy some ghashes, set parameters at the beginning of trader.py file and run it ;)

parameters
==========
* _username_ - username from cex.io
* _apikey_ - apikey generated on cex.io page
* _secret_ - your secret key from cex.io page
* *start_ghs* - the amount of ghs you own and want to be sold by bot
* *start_price* - the starting price (I assume it is the price you paid for ghashes)
* *stop_loss* - how much are you willing to lose, it means sell if current price drops below `start_price*(1-stop_loss)`
* *take_profit* - when to escape if price drops below maximum, it means sell if current price drops below max_price more then `max_price*take_profit)`
