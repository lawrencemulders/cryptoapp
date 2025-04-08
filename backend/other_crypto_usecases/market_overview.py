import requests
import os
from dotenv import load_dotenv

# Generate overview of the market.


def market_overview_crypto():

    local_currency = 'USD'
    local_symbol = '$'

    # Load environment variables from .env file
    load_dotenv()

    api_key = os.getenv("APIKEYCRYPTO")
    headers = {'X-CMC_PRO_API_KEY': api_key}
    base_url = 'https://pro-api.coinmarketcap.com'

    global_url = base_url + '/v1/global-metrics/quotes/latest'

    request = requests.get(global_url, headers=headers)
    results = request.json()

    data = results["data"]

    btc_dominance = data["btc_dominance"]
    eth_dominance = data["eth_dominance"]
    total_market_cap = data["quote"][local_currency]["total_market_cap"]
    total_volume_24h = data["quote"][local_currency]["total_volume_24h"]

    total_market_cap = round(total_market_cap, 2)
    total_volume_24h = round(total_volume_24h, 2)
    btc_dominance = round(btc_dominance, 2)
    eth_dominance = round(eth_dominance, 2)

    total_market_cap_string = local_symbol + '{:,}'.format(total_market_cap)
    total_volume_24h_string = local_symbol + '{:,}'.format(total_volume_24h)

    result = (
        f"The global market cap for all cryptocurrencies is {total_market_cap_string} <br>"
        f"and the global 24h volume is {total_volume_24h_string}.<br><br>"
        f"Bitcoin makes up {btc_dominance}% of the global market cap.<br><br>"
        f"Ethereum makes up {eth_dominance}%."
    )

    print(result)
    return result
