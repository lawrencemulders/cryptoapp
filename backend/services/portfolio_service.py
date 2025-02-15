from backend.db import *


async def get_portfolio():
    return await query_all(
        "SELECT * FROM portfolio ORDER BY 1 ASC"
    )


def add_transaction(user_id, ticker, quantity, is_crypto):
    execute(
        "INSERT INTO portfolio (author_id, ticker, quantity, is_crypto) VALUES (?, ?, ?, ?)",
        user_id, ticker, quantity, is_crypto
    )
