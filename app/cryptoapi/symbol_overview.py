import requests
import json
import os
from dotenv import load_dotenv

# Retrieve specified symbol.


def single_search_crypto():

    local_currency = 'USD'
    local_symbol = '$'

    # Load environment variables from .env file
    load_dotenv()

    api_key = os.getenv("APIKEYCRYPTO")
    headers = {'X-CMC_PRO_API_KEY': api_key}
    base_url = 'https://pro-api.coinmarketcap.com'

    symbol = input("Enter the ticker symbol of a cryptocurrency: ")

    global_url = base_url + '/v1/cryptocurrency/quotes/latest?convert=' + local_currency + '&symbol=' + symbol

    request = requests.get(global_url, headers=headers)
    results = request.json()

    print(json.dumps(results, sort_keys=True, indent=4))

    data = results["data"]
    currency = data[symbol]
    name = currency['name']

    price = currency['quote'][local_currency]['price']
    percent_change_24h = currency['quote'][local_currency]['percent_change_24h']
    market_cap = currency['quote'][local_currency]['market_cap']

    price = round(price, 2)
    percent_change_24h = round(percent_change_24h, 2)
    market_cap = round(market_cap, 2)

    price_string = local_symbol + '{:,}'.format(price)
    percent_change_24h_string = local_symbol + '{:,}'.format(percent_change_24h)
    market_cap_string = local_symbol + '{:,}'.format(market_cap)

    print(name + ' (' + symbol + ') ')
    print('Price: ' + price_string)
    print('24h Change: ' + percent_change_24h_string)
    print('Market Cap: ' + market_cap_string)
    print()
