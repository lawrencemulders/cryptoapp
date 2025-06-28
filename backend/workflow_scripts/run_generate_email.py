from dotenv import load_dotenv
load_dotenv()
import asyncio
from backend.process_flows.table_composer import generate_email_flow


async def main():
    await generate_email_flow()

if __name__ == "__main__":
    asyncio.run(main())
