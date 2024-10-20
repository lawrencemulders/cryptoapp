import aiofiles
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor
import traceback


def process_line(line, table):
    """Process each line from CSV (potentially a blocking operation)."""
    from app.process_flows.table_composer import process_line
    print(f"Processing line: {line}")
    process_line(line, table)


class AsyncManager:
    def __init__(self):
        # Create a ThreadPoolExecutor instance
        self.executor = ThreadPoolExecutor(max_workers=10)

    # Note: Method not in use. Relevant for sentiment url request when replacing Google API
    async def fetch_async(self, url):
        """Fetch data asynchronously from a URL."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    async def process_csv_async(self, csvfile_path, table):
        """Asynchronously read and process the CSV file using threads."""
        loop = asyncio.get_running_loop()
        tasks = []

        # Read the CSV file asynchronously
        async with aiofiles.open(csvfile_path, mode='r', encoding='utf-8') as csv_file:
            async for line in csv_file:
                # Use thread pool to process each line
                try:
                    task = loop.run_in_executor(self.executor, process_line, line.strip().split(','), table)
                    tasks.append(task)
                except Exception as e:
                    print(f"Error processing line {line}: {e}")
                    traceback.print_exc()

        # Await the completion of all thread tasks
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                print(f"Error occurred: {result}")

        print("Processed all lines in csv")

    async def main(self, csvfile_path, table):
        """Main method to manage async CSV processing and other tasks."""
        # Perform async CSV processing
        print(f"Processing {csvfile_path} with {table}")
        await self.process_csv_async(csvfile_path, table)

        # Perform async work (e.g., fetch data from a URL)
        # Note: Method not in use. Relevant for sentiment url request when replacing Google API
        # data = await self.fetch_async("https://example.com")
        # print(f"Fetched data: {data}")

    def run(self, csvfile_path, table):
        """Start the async event loop."""
        try:
            loop = asyncio.get_event_loop()  # Try to get the current event loop
            if loop.is_closed():
                print("Event loop is closed. Creating a new one...")
                loop = asyncio.new_event_loop()  # Create a new loop if closed
                asyncio.set_event_loop(loop)

            loop.run_until_complete(self.main(csvfile_path, table))

        except RuntimeError as e:
            if str(e) == "Event loop is closed":
                print("Event loop was closed. Restarting...")
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.main(csvfile_path, table))
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            traceback.print_exc()
        finally:
            self.executor.shutdown(wait=True)
