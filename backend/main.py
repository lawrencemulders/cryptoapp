from backend.other_crypto_usecases.market_overview import *
from backend.other_crypto_usecases.all_symbols_overview import *
from backend.other_crypto_usecases.symbol_overview import *
from backend.other_crypto_usecases.top_100_overview import *
from backend.other_crypto_usecases.os_alerting import *
from backend.process_flows.table_composer import *

print()
print("Welcome to cryptoapp")
print()

print("This backend creates a periodic notification regarding asset movements and market metrics."
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
    generate_email_flow()
if choice == '2':
    market_overview_crypto()
if choice == '3':
    list_crypto()
if choice == '4':
    single_search_crypto()
if choice == '5':
    top100_crypto()
if choice == '6':
    alert_tracking_crypto()
if choice == '0':
    exit(0)
