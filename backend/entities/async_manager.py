import asyncio
import traceback
from concurrent.futures import ThreadPoolExecutor
from backend.services.portfolio_service import get_portfolio


class AsyncManager:
    def __init__(self, db_dsn):
        """Initialize AsyncManager with a database connection string."""
        self.db_dsn = db_dsn
        self.executor = ThreadPoolExecutor(max_workers=10)

    async def process_assets_async(self, table):
        """Asynchronously process assets from the portfolio database."""
        from backend.process_flows.table_composer import process_line
        loop = asyncio.get_running_loop()
        tasks = []

        portfolio = get_portfolio()

        for asset in portfolio:
            try:
                task = loop.run_in_executor(self.executor, process_line, asset, table)
                tasks.append(task)
            except Exception as e:
                print(f"Error processing asset {asset}: {e}")
                traceback.print_exc()

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for asset, result in zip(portfolio, results):
            if isinstance(result, Exception):
                print(f"Error processing {asset}: {result}")
            else:
                print(f"Successfully processed {asset}")

        print("Finished processing all assets.")

    async def main(self, table):
        """Main method to manage async processing."""
        print(f"Processing portfolio for {table}")
        await self.process_assets_async(table)

    async def run(self, table):
        """Ensure proper async execution."""
        try:
            print("Running async task...")
            await self.main(table)
        except Exception as e:
            print(f"Unexpected error: {e}")
            traceback.print_exc()
        finally:
            print("Shutting down executor...")
            self.executor.shutdown(wait=True)
