from cryptoapi.market_overview import *
from cryptoapi.all_symbols_overview import *
from cryptoapi.symbol_overview import *
from cryptoapi.top_100_overview import *
from cryptoapi.os_alerting import *
from processflows.email_flow import *

config = dotenv_values(".env")
csv_file = config["CSVFILE"]

print()
print("Welcome to cryptoapp")
print()

print("This app creates a periodic notification regarding asset movements and market metrics."
      "\nOther functionality includes deriving market summaries based on user input."
      "\nSelect the preferred option below.")

print()
print("1 - Generate a trial email with portfolio relevant metrics")  # emailgenerator
print("2 - Generic Overview of the Cryptocurrency Market")  # coincap_global
print("3 - List of all Cryptocurrencies")  # coincap_listings
print("4 - Search a Specific Cryptocurrency")  # coincap_quotes
print("5 - Top 100 Cryptocurrency Per Filter")  # top100
print("6 - Alert Tracking of Your Cryptocurrencies")  # alerttracking
print("7 - Generate plist file for email scheduling for macOS")  # plist file to build and run docker container
print("0 - Exit")
print()
choice = input("What is your choice (1-7)? ")

if choice == '1':
    trial_email_flow()
if choice == '2':
    market_overview_crypto()
if choice == '3':
    list_crypto()
if choice == '4':
    single_search_crypto()
if choice == '5':
    top100_crypto()
if choice == '6':
    alert_tracking_crypto(csv_file)
if choice == '7':
    generate_plist_file()
if choice == '0':
    exit(0)
