import csv
import requests
import threading
from processflows.metric_composer import *

# Daily performance of stocks


def time_series_daily_stock(csvfileinput, table):

    api_key = dotenv_values(".env")["APIKEYSTOCK"]

    base_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY'

    with open(csvfileinput, "r", encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        threads = []

        for line in csv_reader:
            thread = threading.Thread(target=process_line, args=(line, base_url, api_key, table))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    return table


def process_line(line, base_url, api_key, table):

    if has_at_least_two_non_empty_columns(line):
        separate_columns = line[0].split(';')
        if "\ufeff" in separate_columns[0]:
            separate_columns[0] = separate_columns[0][1:].upper()
        else:
            separate_columns[0] = separate_columns[0].upper()

        symbol = separate_columns[0]
        amount = separate_columns[1]

        if separate_columns[2] == '1':
            is_crypto = True
        else:
            is_crypto = False

        if is_crypto:
            print("Skipping crypto asset processing")
            return table  # Skip processing and return the original table

        print(f"Successfully read column 1, column 2, and column 3: {symbol}, {amount}, {is_crypto}")

        quote_url = base_url + '&symbol=' + symbol + '&outputsize=compact&apikey=' + api_key

        request = requests.get(quote_url)
        results = request.json()

        print(results)

        table = metric_composer(table, results, symbol, amount, is_crypto)
    else:
        print("Failed to read column 1 and 2")

    return table


def has_at_least_two_non_empty_columns(row, delimiter=';'):

    # Access the string in the list and split it into columns using the specified delimiter
    columns = row[0].split(delimiter)
    return len(columns) >= 2 and all(col.strip() != '' for col in columns)
