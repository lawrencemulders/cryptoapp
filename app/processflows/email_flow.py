from app.communication.generate_email import *
from docker.generate_plist_launchd import generate_plist_file
from app.processflows.metric_composer import *
from prettytable import PrettyTable
from dotenv import load_dotenv
import csv
import requests
import threading
import os


def trial_email_flow():

    #   1) Initialize .env configuration and PrettyTable

    # Load environment variables from .env file
    load_dotenv()

    csvfile = os.getenv("CSVFILE")
    print("Successfully accessed csv")

    table = PrettyTable(['Asset', 'Amount Owned', 'Value', 'Price', '1h', '24h', '7d', 'Sentiment'])

    #  2) Perform API call per row in csvfile

    # Define the path for the CSV file
    if os.path.isfile("/cryptoapp/app/" + csvfile):
        csvfile_path = "/cryptoapp/app/" + csvfile
    elif os.path.isfile("app/" + csvfile):
        csvfile_path = "app/" + csvfile
    else:
        csvfile_path = csvfile

    # Check if the file exists
    if not os.path.isfile(csvfile_path):
        raise FileNotFoundError(f"CSV file not found at path: {csvfile_path}")

    with open(csvfile_path, "r", encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        threads = []

        for line in csv_reader:
            thread = threading.Thread(target=process_line, args=(line, table))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    print("Processed all lines in csv")

    #   3) Generate merge table

    send_email(table)


def schedule_email_flow():

    #   1) Initialize .env configuration, plist file (macOS) and PrettyTable

    csvfile = os.getenv("CSVFILE")
    print("Successfully accessed csv")

    generate_plist_file()

    table = PrettyTable(['Asset', 'Amount Owned', 'Value', 'Price', '1h', '24h', '7d', 'Sentiment'])

    #  2) Iterate for each asset, update table

    # Define the path for the CSV file
    if os.path.isfile("/cryptoapp/app/" + csvfile):
        csvfile_path = "/cryptoapp/app/" + csvfile
    elif os.path.isfile("app/" + csvfile):
        csvfile_path = "app/" + csvfile
    else:
        csvfile_path = csvfile

    # Check if the file exists
    if not os.path.isfile(csvfile_path):
        raise FileNotFoundError(f"CSV file not found at path: {csvfile_path}")

    with open(csvfile_path, "r", encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        threads = []

        for line in csv_reader:
            thread = threading.Thread(target=process_line, args=(line, table))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    print("Processed all lines in csv")

    #   3) Send notification based on schedule config

    schedule.every().sunday.at('12:00').do(send_scheduled_email(table))
    while True:
        schedule.run_pending()
        time.sleep(1)


def process_line(line, table):

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

        print(f"Successfully read column 1, column 2, and column 3: {symbol}, {amount}, {is_crypto}")

        if is_crypto:
            # Perform Crypto api call
            api_key = os.getenv("APIKEYCRYPTO")
            headers = {'X-CMC_PRO_API_KEY': api_key}
            base_url = 'https://pro-api.coinmarketcap.com'

            quote_url = base_url + '/v1/cryptocurrency/quotes/latest?convert=USD&symbol=' + symbol
            request = requests.get(quote_url, headers=headers)
            print("Api call made to Coin Market Cap")
            results = request.json()

        else:
            # Perform Stock api call
            api_key = os.getenv("APIKEYSTOCK")
            base_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY'

            quote_url = base_url + '&symbol=' + symbol + '&outputsize=compact&apikey=' + api_key
            request = requests.get(quote_url)
            print("Api call made to Alpha Vantage")
            results = request.json()

        table = metric_composer(table, results, symbol, amount, is_crypto)

    else:
        print("Failed to read column 1 and 2")

    return table


def has_at_least_two_non_empty_columns(row, delimiter=';'):

    # Access the string in the list and split it into columns using the specified delimiter
    columns = row[0].split(delimiter)
    return len(columns) >= 2 and all(col.strip() != '' for col in columns)
