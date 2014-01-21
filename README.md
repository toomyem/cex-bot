cex-bot
=======
Bot to ease the pain of speculation on CEX.io exchange.

usage
=====
Buy some ghashes, set parameters in the config.py file and run trader.py ;)

parameters
==========
* _username_ - username from cex.io
* _apikey_ - apikey generated on cex.io page
* _secret_ - your secret key from cex.io page
* *ghs* - the amount of ghs you want to be sold by bot
* *limit* - the minimum price limit below which the bot will sell the ghs
* *maximum* - price to activate trailing limit, if the price goes above maximum, the limit is also pushed up
* *delay* - delay in seconds between steps when bot gets data from api (do not set it too low, cex.io limits are 600 queries per 10 minutes)
* *window* - time frame in seconds for mean price calculation
* *debug_mode* - do not atempt to sell anything, just display info
