from backend.db import *


def get_portfolio():
    return query_all(
        "SELECT * FROM portfolio ORDER BY 1 ASC"
    )


def add_transaction(user_id, ticker, quantity, is_crypto):
    execute(
        "INSERT INTO portfolio (author_id, ticker, quantity, is_crypto) VALUES (?, ?, ?, ?)",
        user_id, ticker, quantity, is_crypto
    )
