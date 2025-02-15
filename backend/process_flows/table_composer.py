from backend.communication.send_email import *
from backend.entities.async_manager import *
from backend.entities.crypto_api import CryptoAPI
from backend.entities.stock_api import StockAPI
from backend.process_flows.metric_composer import *
from prettytable import PrettyTable
from collections import namedtuple
import os


PortfolioAsset = namedtuple("PortfolioAsset", ["id", "author_id", "created", "symbol", "amount", "is_crypto"])


async def generate_email_flow():
    """Fetches portfolio, processes assets asynchronously, and sends an email."""

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    database_dir = os.path.join(project_root, 'database')
    db_path = os.path.join(database_dir, 'crypto.db')

    if not db_path:
        raise ValueError("DB_URL is not set in the environment variables")

    print("Successfully found database")

    if db_path.startswith("sqlite:///"):
        db_path = db_path.replace("sqlite:///", "")
        if not os.path.isfile(db_path):
            raise FileNotFoundError(f"Expected SQLite database {db_path} not found")

    # Create table for displaying results
    table = PrettyTable(['Asset', 'Amount Owned', 'Value', 'Price', '1h', '24h', '7d', 'Sentiment'])

    # Initialize AsyncManager
    manager = AsyncManager(db_path)
    await manager.run(table)

    print("Processed all assets in table portfolio")

    # Send email with results
    send_email(table)


def process_line(asset, table):
    """
    Process an asset retrieved from the database.

    asset: Named Tuple containing {id, author_id, created, symbol, amount, is_crypto}
    table: PrettyTable containing data as-is to send to receiver
    """
    try:
        asset = PortfolioAsset(*asset)

        symbol = asset.symbol.upper()
        amount = asset.amount
        is_crypto = asset.is_crypto  # Boolean flag (1 = True, 0 = False)

        print(f"Processing asset: {symbol}, Amount: {amount}, Is Crypto: {is_crypto}")

        # Fetch market data from the correct API
        if is_crypto:
            crypto_api = CryptoAPI(api_key=os.getenv("APIKEYCRYPTO"))
            results = crypto_api.fetch_data(symbol)
        else:
            stock_api = StockAPI(api_key=os.getenv("APIKEYSTOCK"))
            results = stock_api.fetch_data(symbol)

        # Process the fetched data
        table = metric_composer(table, results, symbol, amount, is_crypto)

        print(f"Successfully processed {symbol}")

    except KeyError as e:
        raise Exception(f"Missing expected database column: {e}")
    except Exception as e:
        raise Exception(f"Error processing asset {asset}: {e}")

    return table
