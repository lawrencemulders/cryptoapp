import csv
import requests
import threading
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

    table = PrettyTable(['Asset', 'Amount Owned', 'Value', 'Price', '1h', '24h', '7d', 'Sentiment'])

    with open(csvfileinput, "r", encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        threads = []

        for line in csv_reader:
            thread = threading.Thread(target=process_line, args=(line, base_url, local_currency, headers, table))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    return table


def process_line(line, base_url, local_currency, headers, table):

    if has_at_least_two_non_empty_columns(line):
        separate_columns = line[0].split(';')
        if "\ufeff" in separate_columns[0]:
            separate_columns[0] = separate_columns[0][1:].upper()
        else:
            separate_columns[0] = separate_columns[0].upper()

        symbol = separate_columns[0]
        amount = separate_columns[1]
        print(f"Successfully read column 1 and column 2 {symbol, amount}")

        quote_url = base_url + '/v1/cryptocurrency/quotes/latest?convert=' + local_currency + '&symbol=' + symbol

        request = requests.get(quote_url, headers=headers)
        results = request.json()

        table = metric_composer(table, results, symbol, amount)
    else:
        print(f"Failed to read column 1 and 2")

    return table

def has_at_least_two_non_empty_columns(row, delimiter=';'):

    # Access the string in the list and split it into columns using the specified delimiter
    columns = row[0].split(delimiter)
    return len(columns) >= 2 and all(col.strip() != '' for col in columns)

