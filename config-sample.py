
################################################################
debug_mode = True   # in debug mode nothing will be sold!
log_filename = ""   # file name for log

#################################################################
# data needed to access cex.io api
username = ""
apikey = ""
secret = ""

#################################################################
# settings about trade
ghs     = 1.40      # number of ghs to be sold on price drop
limit   = 0.0462    # limit for stop loss
gap     = 0.0001    # window size
maximum = limit+gap # top price for trailing stop loss
delay   = 10        # delay in secs between steps
window  = 120       # time window for mean price calculation

################################################################
# configuraton for mail notifier
mail_enabled = False
mail_srv     = ""  # mail server address, for example smtp.gmail.com
mail_user    = ""  # user name on mail server
mail_pass    = ""  # password for that user
mail_to      = ""  # who shall receive the information

