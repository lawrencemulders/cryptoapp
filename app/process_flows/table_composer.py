from app.communication.send_email import *
from app.entities.async_manager import *
from app.entities.coinmarketcap_api import CryptoAPI
from app.entities.alphavantage_api import StockAPI
from app.process_flows.metric_composer import *
from prettytable import PrettyTable
from dotenv import load_dotenv
import os


def generate_email_flow():
    load_dotenv()
    csvfile = os.getenv("CSVFILE")
    print("Successfully accessed csv")

    table = PrettyTable(['Asset', 'Amount Owned', 'Value', 'Price', '1h', '24h', '7d', 'Sentiment'])

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

    manager = AsyncManager()
    with open(csvfile_path, "r", encoding='utf-8') as csv_file:
        manager.run(csvfile_path, table)

    print("Processed all lines in csv")

    send_email(table)


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
            crypto_api = CryptoAPI(api_key=os.getenv("APIKEYCRYPTO"))
            results = crypto_api.fetch_data(symbol)
        else:
            # Perform Stock api call
            stock_api = StockAPI(api_key=os.getenv("APIKEYSTOCK"))
            results = stock_api.fetch_data(symbol)

        table = metric_composer(table, results, symbol, amount, is_crypto)
    else:
        raise Exception("Failed to read column 1 and 2")

    return table


def has_at_least_two_non_empty_columns(row, delimiter=';'):
    # Access the string in the list and split it into columns using the specified delimiter
    columns = row[0].split(delimiter)
    return len(columns) >= 2 and all(col.strip() != '' for col in columns)
