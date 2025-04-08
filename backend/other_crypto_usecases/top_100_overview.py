import requests
import os
import prettytable
from colorama import Back, Style
from dotenv import load_dotenv

# Generate top 100 overview based on selected ranking.


def top100_crypto(choice=None):

    global market_cap_string, volume_string
    local_currency = 'USD'
    local_symbol = '$'
    valid_sorts = ['market_cap', 'percent_change_24h', 'volume_24h']

    load_dotenv()
    api_key = os.getenv("APIKEYCRYPTO")
    headers = {'X-CMC_PRO_API_KEY': api_key}
    base_url = 'https://pro-api.coinmarketcap.com'

    if not choice:
        print()
        print("CoinMarketCap Explorer Menu")
        print("1 - Top 100 sorted by market cap")
        print("2 - Top 100 sorted by 24h % change")
        print("3 - Top 100 sorted by 24h volume")
        print("0 - Exit")
        print()

        numeric_choice = input("What is your choice (1-3)? ")
        sort_map = {
            '1': 'market_cap',
            '2': 'percent_change_24h',
            '3': 'volume_24h'
        }

        if numeric_choice == '0':
            exit(0)

        choice = sort_map.get(numeric_choice)
        if not choice:
            return "Invalid choice. Please select 1, 2, or 3."

    if choice not in valid_sorts:
        return "Invalid choice. Please select market_cap, percent_change_24h, or volume_24h."

    quote_url = f"{base_url}/v1/cryptocurrency/listings/latest?convert={local_currency}&sort={choice}"
    request = requests.get(quote_url, headers=headers)
    results = request.json()

    if "data" not in results:
        return f"API Error: {results.get('status', {}).get('error_message', 'Unknown error')}"

    data = results["data"]
    table = prettytable.PrettyTable(['Asset', 'Price', 'Market Cap', 'Volume', '1h', '24h', '7d'])

    for currency in data:
        name = currency['name']
        symbol = currency['symbol']

        quote = currency['quote'][local_currency]
        market_cap = quote['market_cap']
        hour_change = quote['percent_change_1h']
        day_change = quote['percent_change_24h']
        week_change = quote['percent_change_7d']
        price = quote['price']
        volume = quote['volume_24h']

        if hour_change is not None:
            hour_change = round(hour_change, 2)

        if day_change is not None:
            day_change = round(day_change, 2)

        if week_change is not None:
            week_change = round(week_change, 2)

        if volume is not None:
            volume_string = '{:,}'.format(round(volume, 2))

        if market_cap is not None:
            market_cap_string = '{:,}'.format(round(market_cap, 2))

        price_string = '{:,}'.format(round(price, 2))

        table.add_row([name + ' (' + symbol + ')', local_symbol + price_string, local_symbol + market_cap_string,
                       local_symbol + volume_string, str(hour_change), str(day_change), str(week_change)])

    print(table)
    return table
