import os
from dotenv import load_dotenv
import click
from pydapper import connect
import psycopg2
import psycopg2.extras
from flask import g, current_app

load_dotenv()
DB_URL = os.getenv("DB_URL")
print(f"DB_URL: {DB_URL}")


def get_db():
    """Get a connection object attached to Flask `g` context."""
    if 'db_conn' not in g:
        g.db_conn = psycopg2.connect(current_app.config['DB_URL'])
        g.db_conn.autocommit = False
    return g.db_conn


def get_cursor(dict_cursor=True):
    conn = get_db()
    if dict_cursor:
        return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return conn.cursor()


def close_db(e=None):
    """Close db connection in Flask app context."""
    conn = g.pop('db_conn', None)
    if conn is not None:
        conn.close()


def init_db():
    """Run schema SQL on PostgreSQL."""
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(schema_sql)
        conn.commit()


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the PostgreSQL database.")


def query_single(query, *params):
    with connect(DB_URL) as db:
        return db.query_single(query, *params)


def query_all(query, *params):
    with connect(DB_URL) as db:
        return db.query(query, *params)


def execute(query, *params):
    with connect(DB_URL) as db:
        return db.execute(query, *params)


# Flask Integration
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
