import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import click
from flask import g
from pydapper import connect

load_dotenv()
DB_URL = os.getenv("DB_URL")

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
database_dir = os.path.join(project_root, 'database')
db_path = os.path.join(database_dir, 'crypto.db')


# Flask Database Setup
def get_db():
    """Establish a database connection."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # Allows column access by name
    return g.db


def close_db(e=None):
    """Close the database connection."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'schema.sql')

    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_content = f.read()
        db.executescript(schema_content)


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


# Pydapper Queries
def query_single(query, *params):
    with connect(DB_URL) as commands:
        return commands.query_single(query, *params)


async def query_all(query):
    """Execute query and return all results."""
    print(f"Connecting to database at: {db_path}")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        cursor.close()
        conn.close()


def execute(query, *params):
    """Execute query."""
    with connect(DB_URL) as commands:
        return commands.execute(query, *params)


# SQLite3 timestamp converter
sqlite3.register_converter("timestamp", lambda v: datetime.fromisoformat(v.decode()))


def init_app(app):
    """Register database functions with the Flask app. Called by application factory"""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
