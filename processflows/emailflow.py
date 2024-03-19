from communication.emailgenerator import *
from cryptoapi.crypto_portfolio import *
from stockapi.time_series_daily import *
from dotenv import dotenv_values
from prettytable import PrettyTable


def trial_email_flow():

    #   1) Initialize .env configuration and PrettyTable

    csvfile = dotenv_values(".env")["CSVFILE"]

    table = PrettyTable(['Asset', 'Amount Owned', 'Value', 'Price', '1h', '24h', '7d', 'Sentiment'])

    #  2) Perform API calls, iterate per row in csvfile and compose metrics

    cryptoapi_results = portfolio_crypto(csvfile, table)
    stockapi_results = time_series_daily_stock(csvfile, table)

    print("Generated portfolio metrics")

    #   3) Generate merge table

    rows_cryptoapi_results = cryptoapi_results.get_string(header=False).split("\n")[1:]
    rows_stockapi_results = stockapi_results.get_string(header=False).split("\n")[1:]

    merged_table = PrettyTable(['Asset', 'Amount Owned', 'Value', 'Price', '1h', '24h', '7d', 'Sentiment'])

    # Process data from the crypto API
    for row in rows_cryptoapi_results:
        row_data = row.split('|')[1:-1]  # Remove leading and trailing '|' and split by '|'
        row_data = [item.strip() for item in row_data]  # Remove whitespace
        if row_data:
            merged_table.add_row(row_data)

    # Process data from the stock API
    for row in rows_stockapi_results:
        row_data = row.split('|')[1:-1]  # Remove leading and trailing '|' and split by '|'
        row_data = [item.strip() for item in row_data]  # Remove whitespace
        if row_data:
            merged_table.add_row(row_data)

    send_email(merged_table)


def schedule_email_flow_crypto():

    #   1) Initialize .env configuration and PrettyTable

    csvfile = dotenv_values(".env")["CSVFILE"]

    table = PrettyTable(['Asset', 'Amount Owned', 'Value', 'Price', '1h', '24h', '7d', 'Sentiment'])

    #  2) Perform API calls, iterate per row in csvfile and compose metrics

    cryptoapi_results = portfolio_crypto(csvfile, table)
    stockapi_results = time_series_daily_stock(csvfile, table)

    print("Generated portfolio metrics")

    #   3) Generate merge table

    rows_cryptoapi_results = cryptoapi_results.get_string(header=False).split("\n")[1:]
    rows_stockapi_results = stockapi_results.get_string(header=False).split("\n")[1:]

    merged_table = PrettyTable(['Asset', 'Amount Owned', 'Value', 'Price', '1h', '24h', '7d', 'Sentiment'])

    # Process data from the crypto API
    for row in rows_cryptoapi_results:
        row_data = row.split('|')[1:-1]  # Remove leading and trailing '|' and split by '|'
        row_data = [item.strip() for item in row_data]  # Remove whitespace
        if row_data:
            merged_table.add_row(row_data)

    # Process data from the stock API
    for row in rows_stockapi_results:
        row_data = row.split('|')[1:-1]  # Remove leading and trailing '|' and split by '|'
        row_data = [item.strip() for item in row_data]  # Remove whitespace
        if row_data:
            merged_table.add_row(row_data)

    #   4) Send notification based on schedule config

    schedule.every().sunday.at('12:00').do(send_scheduled_email(merged_table))
    while True:
        schedule.run_pending()
        time.sleep(1)
