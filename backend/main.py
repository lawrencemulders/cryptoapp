from backend.other_crypto_usecases.market_overview import *
from backend.other_crypto_usecases.all_symbols_overview import *
from backend.other_crypto_usecases.symbol_overview import *
from backend.other_crypto_usecases.top_100_overview import *
from backend.other_crypto_usecases.os_alerting import *
from backend.process_flows.table_composer import *
from backend.db import *
import asyncio


async def main():
    while True:
        print("Welcome to cryptoapp\n")
        print("This backend creates a periodic notification regarding asset movements and market metrics.")
        print("Other functionality includes deriving market summaries based on user input.")
        print("Select the preferred option below.")
        print("\n1 - Generate a trial email with portfolio relevant metrics")
        print("2 - Generic Overview of the Cryptocurrency Market")
        print("3 - List of all Cryptocurrencies")
        print("4 - Search a Specific Cryptocurrency")
        print("5 - Top 100 Cryptocurrency Per Filter")
        print("6 - Alert Tracking of Your Cryptocurrencies")
        print("7 - Create postgresql database")
        print("0 - Exit")

        choice = input("What is your choice (1-6)? ")

        if choice == '1':
            await generate_email_flow()  # Correctly await the async function
        elif choice == '2':
            market_overview_crypto()  # Synchronous function, no need for await
        elif choice == '3':
            list_crypto()  # Synchronous function, no need for await
        elif choice == '4':
            single_search_crypto()  # Synchronous function, no need for await
        elif choice == '5':
            top100_crypto()  # Synchronous function, no need for await
        elif choice == '6':
            alert_tracking_crypto()  # Synchronous function, no need for await
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid option, please select a valid choice.")


if __name__ == "__main__":
    asyncio.run(main())
