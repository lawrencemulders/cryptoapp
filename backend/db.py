import sqlite3
import os
from datetime import datetime

import click
from flask import current_app
from flask import g


def get_db():
    """Establish a database connection."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
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


sqlite3.register_converter("timestamp", lambda v: datetime.fromisoformat(v.decode()))


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
