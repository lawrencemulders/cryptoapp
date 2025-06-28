import os
from dotenv import load_dotenv
import click
import psycopg2
import psycopg2.extras
from flask import g, current_app
from backend.supabase_client import supabase

# Load environment variables
load_dotenv()
DB_URL = os.getenv("DB_URL")

# ------------------------
# LOCAL PSYCOPG2 USAGE
# ------------------------


def get_db():
    """Get a psycopg2 connection object in Flask `g` context (for local use)."""
    if 'db_conn' not in g:
        g.db_conn = psycopg2.connect(current_app.config['DB_URL'])
        g.db_conn.autocommit = False
    return g.db_conn


def get_cursor(dict_cursor=True):
    """Return a psycopg2 cursor (for local use)."""
    conn = get_db()
    if dict_cursor:
        return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return conn.cursor()


def close_db(e=None):
    """Close psycopg2 connection."""
    conn = g.pop('db_conn', None)
    if conn is not None:
        conn.close()


def init_db():
    """Run schema SQL for local dev only."""
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(schema_sql)
        conn.commit()


@click.command("init-db")
def init_db_command():
    """CLI: Clear data and recreate schema."""
    init_db()
    click.echo("Initialized the PostgreSQL database.")


def init_app(app):
    """Flask app integration."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

# ------------------------
# SUPABASE HTTP API USAGE
# ------------------------


def query_all(table: str, order_by: str = "id"):
    """Select all rows using Supabase HTTP API."""
    result = supabase.table(table).select("*").order(order_by, asc=True).execute()
    return result.data


def query_single(table: str, filter_col: str, value):
    """Select a single row by column using Supabase HTTP API."""
    result = supabase.table(table).select("*").eq(filter_col, value).limit(1).execute()
    return result.data[0] if result.data else None


def insert_row(table: str, row_dict: dict):
    """Insert one row into Supabase table."""
    result = supabase.table(table).insert(row_dict).execute()
    return result.data
