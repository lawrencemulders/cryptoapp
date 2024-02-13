from communication.emailgenerator import *
from cryptoapi.crypto_portfolio import *
from dotenv import dotenv_values


def email_flow_crypto():

    config = dotenv_values(".env")
    csvfile = config["CSVFILE"]

#  2) Perform API calls and compose metrics
#  TODO: define api implementation for stocks and assess retrieved data

    cryptoapi_results = portfolio_crypto(csvfile)

    print("Generated portfolio metrics")

#  3a) Perform necessary calculations
#  TODO: Define metrics

    send_email(cryptoapi_results)


def schedule_email_flow_crypto():

    config = dotenv_values(".env")
    csvfile = config["CSVFILE"]

#  1) Perform API calls and compose metrics
#  TODO: define api implementation for stocks and assess retrieved data

    cryptoapi_results = portfolio_crypto(csvfile)

#  2) Generate scheduled email

    schedule.every().sunday.at('12:00').do(send_scheduled_email(cryptoapi_results))
    while True:
        schedule.run_pending()
        time.sleep(1)
