import os
import sys
import time
import requests
from collections import namedtuple
from datetime import datetime
from dotenv import load_dotenv
from backend.services.portfolio_service import get_portfolio
from backend.supabase_client import supabase

# Load environment variables once at start
load_dotenv()

PortfolioAsset = namedtuple("PortfolioAsset", ["id", "author_id", "created", "symbol", "amount", "is_crypto"])


def alert_tracking_crypto():
    local_currency = 'USD'
    api_key = os.getenv("APIKEYCRYPTO")
    print(f"Loaded APIKEYCRYPTO: {repr(api_key)}")

    if not api_key:
        print("ERROR: APIKEYCRYPTO not found in environment variables.")
        sys.exit(1)

    headers = {'X-CMC_PRO_API_KEY': api_key}
    base_url = 'https://pro-api.coinmarketcap.com'

    print("\nALERTS TRACKING...\n")

    already_hit_symbols = []

    portfolio = get_portfolio()

    while True:
        for asset in portfolio:
            asset = PortfolioAsset(*asset)
            symbol = asset.symbol.upper()
            amount = asset.amount

            quote_url = f"{base_url}/v1/cryptocurrency/quotes/latest?convert={local_currency}&symbol={symbol}"

            try:
                request = requests.get(quote_url, headers=headers)
                request.raise_for_status()  # Raise error on bad status
                results = request.json()
            except Exception as e:
                print(f"Failed to fetch price for {symbol}: {e}")
                continue

            # Check keys exist safely
            if 'data' not in results or symbol not in results['data']:
                print(f"No data for symbol {symbol}")
                continue

            currency = results['data'][symbol]
            name = currency.get('name', 'Unknown')
            price = currency.get('quote', {}).get(local_currency, {}).get('price')

            if price is None:
                print(f"No price data for {symbol}")
                continue

            try:
                price = float(price)
                threshold = float(amount)
            except ValueError:
                print(f"Invalid price or threshold for {symbol}")
                continue

            if price >= threshold and symbol not in already_hit_symbols:
                os.system('say ALERT ALERT ALERT')
                os.system(f'say {name} hit {amount}')
                sys.stdout.flush()

                now = datetime.now()
                current_time = now.strftime("%H:%M")
                print(f"{name} hit {amount} at {current_time}!")
                already_hit_symbols.append(symbol)

        print('...')
        time.sleep(10)
