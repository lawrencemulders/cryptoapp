import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_portfolio():
    response = supabase.table("portfolio").select("*").order("id", desc=False).execute()
    return response.data


def add_transaction(user_id, ticker, quantity, is_crypto):
    data = {
        "author_id": user_id,
        "ticker": ticker,
        "quantity": quantity,
        "is_crypto": is_crypto
    }
    response = supabase.table("portfolio").insert(data).execute()
    return response.data
