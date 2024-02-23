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
print("0 - Exit")
print()
choice = input("What is your choice (1-6)? ")

if choice == '1':
    email_flow_crypto()
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
if choice == '0':
    exit(0)
