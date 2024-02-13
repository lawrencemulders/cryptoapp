from cryptoapi.coincap_global import *
from cryptoapi.coincap_listings import *
from cryptoapi.coincap_quotes import *
from cryptoapi.top100 import *
from cryptoapi.alerttracking import *
from processflows.emailflow import *

config = dotenv_values(".env")
csv_file = config["CSVFILE"]

print()
print("Welcome to cryptoapp")
print()
name = input("What is your name?")

print("Hi " + name + "! ")
print()
print("What would you like to see?")
print("1 - Generic Overview of the Cryptocurrency Market")  # coincap_global
print("2 - List of all Cryptocurrencies")  # coincap_listings
print("3 - Search a Specific Cryptocurrency")  # coincap_quotes
print("4 - Top 100 Cryptocurrency Per Filter")  # top100
print("5 - Alert Tracking of Your Cryptocurrencies")  # alerttracking
print("6 - Generate a trial email with portfolio relevant metrics")  # emailgenerator
print("0 - Exit")
print()
choice = input("What is your choice(1-7)? ")

if choice == '1':
    market_overview_crypto()
if choice == '2':
    list_crypto()
if choice == '3':
    single_search_crypto()
if choice == '4':
    top100_crypto()
if choice == '5':
    alert_tracking_crypto(csv_file)
if choice == '6':
    email_flow_crypto()
if choice == '0':
    exit(0)
