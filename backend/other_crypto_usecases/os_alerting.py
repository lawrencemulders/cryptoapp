import os
import sys
import time
import requests
from collections import namedtuple
from datetime import datetime
from dotenv import load_dotenv
from backend.services.portfolio_service import get_portfolio


# Trigger alerts when price enters a predefined threshold. CSV file is used as source.

PortfolioAsset = namedtuple("PortfolioAsset", ["id", "author_id", "created", "symbol", "amount", "is_crypto"])


def alert_tracking_crypto():
    local_currency = 'USD'
    load_dotenv()
    api_key = os.getenv("APIKEYCRYPTO")
    headers = {'X-CMC_PRO_API_KEY': api_key}
    base_url = 'https://pro-api.coinmarketcap.com'

    print()
    print("ALERTS TRACKING...")
    print()

    already_hit_symbols = []
    portfolio = get_portfolio()

    while True:

        for asset in portfolio:

            asset = PortfolioAsset(*asset)
            symbol = asset.symbol.upper()
            amount = asset.amount

            quote_url = (base_url + '/v1/cryptocurrency/quotes/latest?convert=' + local_currency + '&symbol=' + symbol)
            request = requests.get(quote_url, headers=headers)
            results = request.json()

            currency = results['data'][symbol]

            name = currency['name']
            price = currency['quote'][local_currency]['price']

            if float(price) >= float(amount) and symbol not in already_hit_symbols:
                os.system('say ALERT ALERT ALERT')
                os.system('say ' + name + ' hit ' + amount)
                sys.stdout.flush()

                now = datetime.now()
                current_time = now.strftime("%H:%M")
                print(name + ' hit ' + amount + ' at ' + current_time + '!')
                already_hit_symbols.append(symbol)

        print('...')
        time.sleep(10)
