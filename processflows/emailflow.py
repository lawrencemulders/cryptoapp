from communication.emailgenerator import *
from cryptoapi.crypto_portfolio import *
from dotenv import dotenv_values


def email_flow_crypto():

    config = dotenv_values(".env")
    csvfile = config["CSVFILE"]

    #  with open(csvfile, "r") as csv_file:
    #   csv_reader = csv.reader(csv_file)
    #    for line in csv_reader:
    #        if "\ufeff" in line[0]:
    #            line[0] = line[0][1:].upper()
    #        else:
    #            line[0] = line[0].upper()

    #        symbol = line[0]
    #        amount = line[1]

#  2) Perform API calls
#  TODO: define api implementation for stocks and assess retrieved data
#  TODO: establish mapping between api results and local variables

    cryptoapi_results = cryptoportfolio(csvfile)

    print("Generated portfolio metrics")

#  3a) Perform necessary calculations
#  TODO: Define metrics

#  3b) Persist upon csv file


#  5) Retrieve data from csv file


#  6) Generate 1 off email

    send_email(cryptoapi_results)


def schedule_email_flow_crypto():

    config = dotenv_values(".env")
    csvfile = config["CSVFILE"]

    with open(csvfile, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            if "\ufeff" in line[0]:
                line[0] = line[0][1:].upper()
            else:
                line[0] = line[0].upper()

            symbol = line[0]
            amount = line[1]

#  2) Perform API calls
#  TODO: define api implementation for stocks and assess retrieved data
#  TODO: establish mapping between api results and local variables

        cryptoapi_results = cryptoportfolio(csvfile)

#  3a) Perform necessary calculations
#  TODO: Define metrics

#  3b) Persist upon csv file


#  5) Retrieve data from csv file


#  6) Generate scheduled email

    schedule.every().sunday.at('12:00').do(send_scheduled_email(cryptoapi_results))
    while True:
        schedule.run_pending()
        time.sleep(1)