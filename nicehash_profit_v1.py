import requests
import json
import time
from datetime import datetime
from exchanges.bitstamp import Bitstamp
from decimal import Decimal


def get_balance():
    r = requests.get('https://api.nicehash.com/api?method=stats.provider&addr=3Cf6fCcrEf4Jkj69imdcQkwqQx2khEm6J5')
    r = json.loads(r.text)
    stats = r['result']['stats']
    total = 0
    for algo in stats:
        total += Decimal(algo['balance'])
    return total

startTime = datetime.now()
print startTime
starting_balance = get_balance()
print "Starting balance: " + str(starting_balance)

while True:
    try:
        time.sleep(60)
        seconds = Decimal((datetime.now() - startTime).total_seconds())
        earnings = get_balance() - starting_balance
        per_day = 60*60*24*earnings/seconds
        bitcoin_price = Bitstamp().get_current_price()
        print('Earnings: ' + str(earnings) + ' (' + str(earnings*bitcoin_price) + ' USD)  ' + str(per_day) + '( ' +
              str(per_day*bitcoin_price) + ' USD) / Day')
    except Exception, e:
        print 'We had an issue ' + str(e)
# print total * bitcoin_price
