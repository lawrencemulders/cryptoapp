import requests
from prettytable import PrettyTable
from colorama import Back, Style
from dotenv import dotenv_values


# Ranking of coins based on filters


def top100_crypto():
    local_currency = 'USD'
    local_symbol = '$'

    config = dotenv_values(".env")
    api_key = config["APIKEY"]
    headers = {'X-CMC_PRO_API_KEY': api_key}

    base_url = 'https://pro-api.coinmarketcap.com'

    print()
    print("CoinMarketCap Explorer Menu")
    print()
    print("1 - Top 100 sorted by market cap")
    print("2 - Top 100 sorted by 24h % change")
    print("3 - Top 100 sorted by 24h volume")
    print("0 - Exit")
    print()

    choice = input("What is your choice(1-3)? ")

    sort = ""

    if choice == '1':
        sort = 'market_cap'
    if choice == '2':
        sort = 'percent_change_24h'
    if choice == '3':
        sort = 'volume_24h'
    if choice == '0':
        exit(0)

    quote_url = base_url + '/v1/cryptocurrency/listings/latest?convert=' + local_currency + '&sort=' + sort

    request = requests.get(quote_url, headers=headers)
    results = request.json()

# print(json.dumps(results, sort_keys=True, indent=4))

    data = results["data"]

    table = PrettyTable(['Asset', 'Price', 'Market Cap', 'Volume', '1h', '24h', '7d'])

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
            if hour_change > 0:
                hour_change = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
            else:
                hour_change = Back.RED + str(hour_change) + '%' + Style.RESET_ALL

        if day_change is not None:
            day_change = round(day_change, 2)
            if day_change > 0:
                day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
            else:
                day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL

        if week_change is not None:
            week_change = round(week_change, 2)
            if week_change > 0:
                week_change = Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
            else:
                week_change = Back.RED + str(week_change) + '%' + Style.RESET_ALL

        if volume is not None:
            volume_string = '{:,}'.format(round(volume, 2))

        if market_cap is not None:
            market_cap_string = '{:,}'.format(round(market_cap, 2))

        price_string = '{:,}'.format(round(price, 2))

        table.add_row([name + ' (' + symbol + ')',
                        local_symbol + price_string,
                        local_symbol + market_cap_string,
                        local_symbol + volume_string,
                        str(hour_change),
                        str(day_change),
                        str(week_change)])

    print()
    print(table)
    print()
