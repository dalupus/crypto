import requests
import json
import time
import traceback
from datetime import datetime
from exchanges.bitstamp import Bitstamp
from decimal import Decimal

algos = []


def get_balance():
    global algos, profitability
    r = requests.get('https://api.nicehash.com/api?method=stats.provider.ex&addr=3Cf6fCcrEf4Jkj69imdcQkwqQx2khEm6J5')
    r = json.loads(r.text)
    stats = r['result']['current']
    algos = []
    total = 0
    for algo in stats:
        total += float(algo['data'][1])
        if algo['data'][0]:
            name = algo['name']
            algos += [name]
    return float(total)


startTime = datetime.now()
print(startTime)
starting_balance = get_balance()
print("Starting balance: " + str(starting_balance))

while True:
    try:
        time.sleep(60)
        seconds = (datetime.now() - startTime).total_seconds()
        earnings = get_balance() - starting_balance
        per_day = 60 * 60 * 24 * earnings / seconds
        bitcoin_price = float(Bitstamp().get_current_price())
        output = '{:%Y-%m-%d %H:%M:%S} Earnings: {:.7f}  {:.8f} ({:.4f} USD) ' \
                 '{:.8f} ({:.4f} USD) / Day  {}\t'.format(datetime.now(),
                                                              earnings + starting_balance,
                                                              earnings,
                                                              earnings * bitcoin_price,
                                                              per_day,
                                                              per_day * bitcoin_price,
                                                              algos,
                                                              )
        # print('Earnings: ' + str(earnings) + ' (' + str(earnings * bitcoin_price) + ' USD)  ' + str(per_day) + '( ' +
        #       str(per_day * bitcoin_price) + ' USD) / Day')
        print(output)
    except Exception as e:
        print('We had an issue ' + str(e))
        print(traceback.format_exc())
# print total * bitcoin_price
