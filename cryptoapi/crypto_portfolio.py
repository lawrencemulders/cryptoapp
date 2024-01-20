import csv
import requests
from prettytable import PrettyTable
from colorama import Back, Style
from dotenv import dotenv_values


# Performance of a portfolio using a csv file as source


def cryptoportfolio(csvfileinput):
    local_currency = 'USD'
    local_symbol = '$'

    config = dotenv_values(".env")
    api_key = config["APIKEY"]

    headers = {'X-CMC_PRO_API_KEY': api_key}

    base_url = 'https://pro-api.coinmarketcap.com'

    print()
    print("My Portfolio")
    print()

    portfolio_value = 0.00

    table = PrettyTable(['Asset', 'Amount Owned', 'Value', 'Price', '1h', '24h', '7d'])

    with open(csvfileinput, "r", encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        print(csv_reader)
        for line in csv_reader:
            if has_at_least_two_non_empty_columns(line):  # Check if the line has at least 2 elements
                seperate_columns = line[0].split(';')
                if "\ufeff" in seperate_columns[0]:
                    seperate_columns[0] = seperate_columns[0][1:].upper()
                else:
                    seperate_columns[0] = seperate_columns[0].upper()

                symbol = seperate_columns[0]
                amount = seperate_columns[1]
                print(f"Successfully read column 1 and column 2 {symbol, amount}")
            else:
                print(f"Failed to read column 1 and 2")
                continue

            quote_url = base_url + '/v1/cryptocurrency/quotes/latest?convert=' + local_currency + '&symbol=' + symbol

            request = requests.get(quote_url, headers=headers)
            results = request.json()

            # print(json.dumps(results, sort_keys=True, indent=4))

            try:
                currency = results['data'][symbol]
            except KeyError:
                continue

            name = currency['name']

            quote = currency['quote'][local_currency]

            hour_change = round(quote['percent_change_1h'], 1)
            day_change = round(quote['percent_change_24h'], 1)
            week_change = round(quote['percent_change_7d'], 1)

            price = quote['price']

            value = float(price) * float(amount)

            portfolio_value += value

            if hour_change > 0:
                hour_change = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
            else:
                hour_change = Back.RED + str(hour_change) + '%' + Style.RESET_ALL

            if day_change > 0:
                day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
            else:
                day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL

            if week_change > 0:
                week_change = Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
            else:
                week_change = Back.RED + str(week_change) + '%' + Style.RESET_ALL

            price_string = '{:,}'.format(round(price, 2))
            value_string = '{:,}'.format(round(value, 2))

            table.add_row([name + ' (' + symbol + ')',
                           amount,
                           local_symbol + value_string,
                           local_symbol + price_string,
                           str(hour_change),
                           str(day_change),
                           str(week_change)])
            print(f"Added new row to table: {table}")
    return table

def has_at_least_two_non_empty_columns(row, delimiter=';'):
    # Access the string in the list and split it into columns using the specified delimiter
    columns = row[0].split(delimiter)
    return len(columns) >= 2 and all(col.strip() != '' for col in columns)

