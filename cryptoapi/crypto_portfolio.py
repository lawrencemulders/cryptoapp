import csv
import requests
from dotenv import dotenv_values
from prettytable import PrettyTable
from processflows.metric_composer import *


# Performance of a portfolio using a csv file as source


def portfolio_crypto(csvfileinput):
    local_currency = 'USD'

    config = dotenv_values(".env")
    api_key = config["APIKEY"]

    headers = {'X-CMC_PRO_API_KEY': api_key}

    base_url = 'https://pro-api.coinmarketcap.com'

    print()
    print("My Portfolio")
    print()

    table = PrettyTable(['Asset', 'Amount Owned', 'Value', 'Price', '1h', '24h', '7d', 'Sentiment'])

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

            table = metric_composer(table, results, symbol, amount)

            # print(json.dumps(results, sort_keys=True, indent=4))
    return table

def has_at_least_two_non_empty_columns(row, delimiter=';'):
    # Access the string in the list and split it into columns using the specified delimiter
    columns = row[0].split(delimiter)
    return len(columns) >= 2 and all(col.strip() != '' for col in columns)

